# Extracto saneado del log humano de 0.8.1 (dusklight-20261102-081838, 8 mods) [R]

Copia temporal leída con permiso y borrada después. Prefijo `Lnnnn` = número de línea original. Sin rutas, cuentas ni marcas de tiempo; las líneas de Expansion van recortadas.

## Resúmenes de cierre
```
L9412 POST08_SUMMARY v=0.8.1 tag=SHUTDOWN part=1/3 parry=ON layout=MATCHES_EXE window=[-1,+9]f/11t ticks=11003 shield_attacks_started=51 shield_attacks_ended=51 sa_with_enemy_contact=47 sa_with_native_block=47 sa_with_parry=22 link_changes=3 judged=79430 episodes=153 contacts_verified=5646 blocked_during_shield_attack=551 transitioned_after_block=57
L9413 POST08_SUMMARY v=0.8.1 tag=SHUTDOWN part=2/3 candidates=23 normal_guard=287 not_blocked=4 missed_early=3 missed_late=2 duplicate=0 latched=0 fury_chip_refused=0 not_attacking=4922 untracked=405 link_invalid=0 no_pass_snapshot=0 event_running=0
L9414 POST08_SUMMARY v=0.8.1 tag=SHUTDOWN part=3/3 commit_attempts=23 parries_committed=23 posture_units=846 breaks_by_parry=6 stun_suppressed=0 unexpected_hp_delta=0 write_failed=0 link_life_drop_next_tick=0 px_parries=23 px_parry_units=846 px_parry_crossings=6 posture_audit_ok=1 e6_parry=1 invariant_ok=1 lines(contact/sa)=250+5188_dropped/102+0_dropped timing_delta_hist_frames={0:42,1:39,2:43,3:40,4:42,5:39,6:38,7:39,8:39,9:38,10:38,11:38,12:38,13:38}
L9407 POST05_SUMMARY v=0.6.0 tag=SHUTDOWN decisions=116 duplicates=0 not_applicable=11 allow_vanilla=39 skip_unsafe=0 eligible=66 confirmed=105 attempted=66 applied=66 recheck_failed=0 verify_failed=0 not_attempted=0 applied_by_pre_state(0/1/2)=8/14/10 session_disabled=0 log(written/dropped)=105/0 resource(e_oc/e_oc2/other)=70/46/0 e2_policy=MATURE_BC_OR_BRAKE e2_phase(na/anim/startup/early/ending
L9410 POST06_SUMMARY v=0.8.0 tag=SHUTDOWN calls=79430 breaks=19 shields=14 bonus=12 timeouts=0 native_stun_ends=7 rearms50=7 rearms0=1 rearms0_redirected=1 failed=0
```

## Los 23 CONFIRMED (frame del enemigo, Link en la pasada/ahora, transición)
```
L2104 attacker_id=163 generation=10 pass_proc=30 sa_age_ticks=7 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.25 enemy_rate=1.15 posture_before=0 posture_after=40 crossed=0
L2427 attacker_id=163 generation=10 pass_proc=30 sa_age_ticks=2 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=17.10 enemy_rate=1.15 posture_before=41 posture_after=81 crossed=0
L2523 attacker_id=161 generation=8 pass_proc=30 sa_age_ticks=4 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.00 enemy_rate=1.00 posture_before=0 posture_after=40 crossed=0
L2679 attacker_id=162 generation=9 pass_proc=30 sa_age_ticks=2 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=17.00 enemy_rate=1.00 posture_before=0 posture_after=40 crossed=0
L2769 attacker_id=218 generation=2 pass_proc=30 sa_age_ticks=4 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.25 enemy_rate=1.15 posture_before=0 posture_after=40 crossed=0
L2987 attacker_id=221 generation=3 pass_proc=30 sa_age_ticks=0 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=15.95 enemy_rate=1.15 posture_before=0 posture_after=40 crossed=0
L3040 attacker_id=221 generation=3 pass_proc=30 sa_age_ticks=2 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.25 enemy_rate=1.15 posture_before=61 posture_after=100 crossed=1
L3064 attacker_id=221 generation=3 pass_proc=30 sa_age_ticks=9 now_proc=30 transitioned=0 enemy_state=2 enemy_frame=1.00 enemy_rate=1.15 posture_before=75 posture_after=100 crossed=1
L3149 attacker_id=222 generation=4 pass_proc=30 sa_age_ticks=5 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=18.00 enemy_rate=1.00 posture_before=14 posture_after=54 crossed=0
L3171 attacker_id=222 generation=4 pass_proc=30 sa_age_ticks=2 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=17.00 enemy_rate=1.00 posture_before=70 posture_after=100 crossed=1
L4022 attacker_id=284 generation=11 pass_proc=30 sa_age_ticks=4 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=18.00 enemy_rate=1.00 posture_before=0 posture_after=40 crossed=0
L4042 attacker_id=284 generation=11 pass_proc=30 sa_age_ticks=3 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.00 enemy_rate=1.00 posture_before=65 posture_after=100 crossed=1
L4186 attacker_id=341 generation=12 pass_proc=30 sa_age_ticks=2 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=17.00 enemy_rate=1.00 posture_before=50 posture_after=90 crossed=0
L4271 attacker_id=341 generation=12 pass_proc=30 sa_age_ticks=4 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=18.00 enemy_rate=1.00 posture_before=73 posture_after=100 crossed=1
L7712 attacker_id=836 generation=35 pass_proc=30 sa_age_ticks=8 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=15.95 enemy_rate=1.15 posture_before=0 posture_after=40 crossed=0
L7927 attacker_id=838 generation=37 pass_proc=30 sa_age_ticks=0 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=15.95 enemy_rate=1.15 posture_before=58 posture_after=98 crossed=0
L8311 attacker_id=836 generation=35 pass_proc=30 sa_age_ticks=7 now_proc=30 transitioned=0 enemy_state=2 enemy_frame=1.00 enemy_rate=1.15 posture_before=50 posture_after=90 crossed=0
L8439 attacker_id=836 generation=35 pass_proc=30 sa_age_ticks=1 now_proc=30 transitioned=0 enemy_state=1 enemy_frame=1.00 enemy_rate=1.15 posture_before=50 posture_after=90 crossed=0
L8606 attacker_id=836 generation=35 pass_proc=30 sa_age_ticks=4 now_proc=30 transitioned=0 enemy_state=1 enemy_frame=1.00 enemy_rate=1.15 posture_before=90 posture_after=100 crossed=1
L8613 attacker_id=838 generation=37 pass_proc=30 sa_age_ticks=6 now_proc=30 transitioned=0 enemy_state=2 enemy_frame=1.00 enemy_rate=1.00 posture_before=32 posture_after=72 crossed=0
L8689 attacker_id=836 generation=35 pass_proc=30 sa_age_ticks=9 now_proc=30 transitioned=0 enemy_state=1 enemy_frame=1.00 enemy_rate=1.15 posture_before=50 posture_after=90 crossed=0
L9088 attacker_id=838 generation=37 pass_proc=30 sa_age_ticks=1 now_proc=29 transitioned=1 enemy_state=1 enemy_frame=17.10 enemy_rate=1.15 posture_before=38 posture_after=78 crossed=0
L9171 attacker_id=893 generation=29 pass_proc=30 sa_age_ticks=3 now_proc=29 transitioned=1 enemy_state=2 enemy_frame=18.25 enemy_rate=1.15 posture_before=0 posture_after=40 crossed=0
```

## Actor 836 tras el parry falso de L8311: golpes que empiezan (ATTACK 4/1-2) y vuelven a FIND/4 sin completarse
```
L8320 POST08_SHIELD_ATTACK_END sa_serial=40 tick=8797 duration_ticks=14 last_frame=14.00 exit_proc=6 contacts=28 blocks=28 parries=1
L8381 POST08_SHIELD_ATTACK_END sa_serial=41 tick=8843 duration_ticks=14 last_frame=14.00 exit_proc=7 contacts=28 blocks=28 parries=0
L8458 POST08_SHIELD_ATTACK_END sa_serial=42 tick=8903 duration_ticks=14 last_frame=14.00 exit_proc=7 contacts=28 blocks=28 parries=1
L8625 POST08_SHIELD_ATTACK_END sa_serial=43 tick=9020 duration_ticks=14 last_frame=14.00 exit_proc=7 contacts=28 blocks=28 parries=2
L8669 POST08_SHIELD_ATTACK_END sa_serial=44 tick=9057 duration_ticks=14 last_frame=14.00 exit_proc=7 contacts=28 blocks=28 parries=0
L8696 POST08_SHIELD_ATTACK_END sa_serial=45 tick=9078 duration_ticks=14 last_frame=14.00 exit_proc=7 contacts=28 blocks=28 parries=1
```
