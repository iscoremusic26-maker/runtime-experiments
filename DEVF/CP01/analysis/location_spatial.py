from verify_footprint import *
def triangle_box(tri,lo,hi):
    center=tuple((a+b)/2 for a,b in zip(lo,hi));extent=tuple((b-a)/2 for a,b in zip(lo,hi))
    v=[tuple(a-b for a,b in zip(p,center)) for p in tri]
    edges=[tuple(b-a for a,b in zip(v[i],v[(i+1)%3])) for i in range(3)]
    axes=[(1,0,0),(0,1,0),(0,0,1),cross(edges[0],edges[1])]
    axes += [cross(e,a) for e in edges for a in [(1,0,0),(0,1,0),(0,0,1)]]
    for axis in axes:
        q=[dot(p,axis) for p in v];r=dot(extent,tuple(abs(x) for x in axis))
        if min(q)>r+1e-6 or max(q)<-r-1e-6:return False
    return True
def boxgap(poly,center,half,yaw):
    a=yaw*2*math.pi/65536;co,si=math.cos(a),math.sin(a)
    local=[(co*(x-center[0])-si*(z-center[2]),si*(x-center[0])+co*(z-center[2])) for x,z in poly]
    # Four separating axes of the two rectangles. Positive gap proves XZ separation.
    other=[(co*x+si*z+center[0],-si*x+co*z+center[2]) for x in [-half[0],half[1]] for z in [-half[2],half[3]]]
    gaps=[min(q[0] for q in local)-half[1],-half[0]-max(q[0] for q in local),min(q[1] for q in local)-half[3],-half[2]-max(q[1] for q in local),min(q[0] for q in other)-max(q[0] for q in poly),min(q[0] for q in poly)-max(q[0] for q in other),min(q[1] for q in other)-max(q[1] for q in poly),min(q[1] for q in poly)-max(q[1] for q in other)]
    return max(gaps)
def point_rect_distance(p,poly):
    lo=[min(x[i] for x in poly) for i in range(2)];hi=[max(x[i] for x in poly) for i in range(2)]
    return math.hypot(max(lo[0]-p[0],0,p[0]-hi[0]),max(lo[1]-p[2],0,p[2]-hi[1]))
def path_rect_distance(path,poly):
    segments=list(zip(path['points'],path['points'][1:]))+([(path['points'][-1],path['points'][0])] if path['closed'] else [])
    distances=[point_rect_distance(p,poly) for p in path['points']]
    for a,b in segments:
        # Exact segment-to-rectangle: clipping detects crossings; otherwise endpoints/edges.
        t0,t1=0,1
        for axis in [0,1]:
            j=0 if axis==0 else 2;v=b[j]-a[j]
            lo=min(q[axis] for q in poly);hi=max(q[axis] for q in poly)
            if abs(v)<1e-12:
                if a[j]<lo or a[j]>hi:t0,t1=1,0;break
            else:
                s0,s1=sorted([(lo-a[j])/v,(hi-a[j])/v]);t0=max(t0,s0);t1=min(t1,s1)
        if t0<=t1:return 0
        distances += [point_distance_segment((q[0],0,q[1]),a,b) for q in poly]
    return min(distances,default=None)
if __name__=='__main__':
    fp=json.loads((ROOT/'footprint-verification.json').read_text());p=fp['candidate'];poly=fp['footprints']['model_and_collision']['rectangle']
    inv=json.loads((ROOT/'inventory.json').read_text())
    room=ROOT/'R03_00.arc';meta,tris=kcl((room/'kcl/room.kcl').read_bytes(),(room/'plc/room.plc').read_bytes())
    lo=(poly[0][0],p[1],poly[0][1]);hi=(poly[2][0],p[1]+429.4033508300781,poly[2][1])
    overlaps=[t for t in tris if triangle_box(t['pts'],lo,hi)]
    result=dict(static_kcl_box_overlap_count=len(overlaps),static_kcl_ground_overlap_prisms=[t['index'] for t in overlaps if t['normal'][1]>=.5],static_kcl_wall_or_roof_overlap_prisms=[t['index'] for t in overlaps if t['normal'][1]<.5],volumes=[],actor_counts={},nearest_actors={},nearest_routes={})
    for arc,an in [('R03_00.arc','dzr/room.dzr'),('STG_00.arc','dzs/stage.dzs')]:
        file=next(f for f in inv['archives'][arc]['files'] if 'chunks' in f)
        active=[(c,e) for c in file['chunks'] if c['tag'] in ['ACTR','TGOB','ACT6','TGSC','SCOB','SCO6','TGDR','Door','Doo6','TRE6'] for e in c['records']]
        result['actor_counts'][arc]=dict(common=sum(c['count'] for c in file['chunks'] if c['tag'] in ['ACTR','TGOB','TGSC','SCOB','TGDR','Door']),layer6=sum(c['count'] for c in file['chunks'] if c['tag'] in ['ACT6','SCO6','Doo6','TRE6']),potential_records=len(active),layers_with_actor_chunks=[c['tag'] for c in file['chunks'] if c['tag'].startswith(('ACT','SCO'))])
        nearest=[]
        for c,e in active:
            dist=math.hypot(e['position'][0]-p[0],e['position'][2]-p[2])
            nearest.append(dict(tag=c['tag'],index=e['index'],name=e['name'],parameters=e['parameters'],distance_xz=dist))
            sb=e['scale_bytes']
            if sb is None:continue
            s=[x/10 for x in sb];name=e['name'];param=int(e['parameters'],16);pos=e['position'];yaw=e['angle'][1];entry=dict(archive=arc,tag=c['tag'],index=e['index'],name=name,parameters=e['parameters'],center=pos,angle_y=yaw,scale=s)
            if name=='scnChg':
                half=[s[0]*75,s[0]*75,s[2]*75,s[2]*75];entry.update(shape='yaw_box',half_xz=half,y_interval=[pos[1],pos[1]+s[1]*150],separating_gap_xz=boxgap(poly,pos,half,yaw))
            elif name=='noChgRm':
                mult=1000 if ((param>>8)&15) else 100
                half=[s[0]*mult,s[0]*mult,s[2]*mult,s[2]*mult];entry.update(shape='yaw_box',half_xz=half,y_interval=[pos[1],pos[1]+s[1]*mult],separating_gap_xz=boxgap(poly,pos,half,yaw))
            elif name=='RMback0':
                half=[s[0]*100,s[0]*100,s[2]*100,s[2]*100];entry.update(shape='yaw_box_y_ignored',half_xz=half,separating_gap_xz=boxgap(poly,pos,half,yaw))
            elif name=='atkItem':
                radius=s[0]*50;entry.update(shape='attack_cylinder',radius=radius,y_interval=[pos[1]-s[1]*100,pos[1]],separating_gap_xz=point_rect_distance(pos,poly)-radius)
            elif name=='SwAreaS' and (param>>18)&3==0:
                mult=10 if (param>>20)&15==1 else 1
                half=[s[0]*mult*50,s[0]*mult*50,s[2]*mult*50,s[2]*mult*50]
                entry.update(shape='yaw_box',half_xz=half,y_interval=[pos[1],pos[1]+s[1]*mult*100],separating_gap_xz=boxgap(poly,pos,half,yaw))
            elif name=='EvtArea':
                typ=e['angle'][2]&255
                assert typ==21
                half=[s[0]*1000,s[0]*1000,s[2]*1000,s[2]*1000]
                entry.update(shape='conservative_type21_xz_box',half_xz=half,separating_gap_xz=boxgap(poly,pos,half,yaw))
            elif name=='hider':
                mult=1250 if param>>30 else 125
                half=[s[0]*mult,s[0]*mult,s[2]*mult,s[2]*mult]
                entry.update(shape='axis_aligned_suspend_box',half_xz=half,y_interval=[pos[1],pos[1]+s[1]*mult*2],separating_gap_xz=boxgap(poly,pos,half,0))
            elif name=='KY_chg' and ((param>>24)&15)==5:
                radius=s[0]*5000
                entry.update(shape='weather_type5_radius',radius=radius,separating_gap_xz=point_rect_distance(pos,poly)-radius)
            elif name in ['ClearB','KY_chg']:
                entry.update(shape='not_certified_by_generic_scale',status='CONTEXT_OR_EXTERNAL_RESOURCE_REQUIRED')
            else:entry.update(shape='UNRESOLVED',status='NOT_VERIFIED')
            result['volumes'].append(entry)
        result['nearest_actors'][arc]=sorted(nearest,key=lambda x:x['distance_xz'])[:7]
        ps=paths((ROOT/arc/an).read_bytes())
        distances=[dict(index=x['index'],distance_to_model_rectangle_xz=path_rect_distance(x,poly),count=x['count'],closed=x['closed']) for x in ps if x['points']]
        result['nearest_routes'][arc]=sorted(distances,key=lambda x:x['distance_to_model_rectangle_xz'])[:5]
    assert not result['static_kcl_wall_or_roof_overlap_prisms']
    assert all(e.get('separating_gap_xz',1)>0 for e in result['volumes'])
    (ROOT/'spatial.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS selected volume XZ separation; static KCL wall/roof intersections:',len(result['static_kcl_wall_or_roof_overlap_prisms']),'(dynamic/global effects not certified)')
