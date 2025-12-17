if cur is not None:
            prev_attack = current_attack
            finished = (cur.update() == False)
            if finished:
                # if the final wait attack just finished, show win screen
                if prev_attack == "attack_wait_2":
                    pygame.mixer.music.stop()
                    win_screen()
                    # after win_screen returns, halt the sequence
                    current_attack = "none"
                else:
                    # advance sequence as before
                    if current_attack == "attack0":
                        current_attack = "attack1"
                    elif current_attack == "attack1":
                        current_attack = "attack2"
                    elif current_attack == "attack2":
                        current_attack = "attack3"
                    elif current_attack == "attack3":
                        current_attack = "attack4"
                    elif current_attack == "attack4":
                        current_attack = "attack5"
                    elif current_attack == "attack5":
                        current_attack = "attack6"
                    elif current_attack == "attack6":
                        current_attack = "attack7"
                    elif current_attack == "attack7":
                        current_attack = "attack8"
                    elif current_attack == "attack8":
                        current_attack = "attack9"
                    elif current_attack == "attack9":
                        current_attack = "attack10"
                    elif current_attack == "attack10":
                        current_attack = "attack11"
                    elif current_attack == "attack11":
                        current_attack = "attack12"
                    elif current_attack == "attack12":
                        current_attack = "attack13"
                    elif current_attack == "attack13":
                        current_attack = "attack14"
                    elif current_attack == "attack14":
                        current_attack = "attack15"
                    elif current_attack == "attack15":
                        current_attack = "attack_wait"
                    elif current_attack == "attack_wait":
                        current_attack = "attack16"
                    elif current_attack == "attack16":
                        current_attack = "attack17"
                    elif current_attack == "attack17":
                        current_attack = "attack18"
                    elif current_attack == "attack18":
                        current_attack = "attack19"
                    elif current_attack == "attack19":
                        current_attack = "attack20"
                    elif current_attack == "attack20":
                        current_attack = "attack21"
                    elif current_attack == "attack21":
                        current_attack = "attack_wait_2"
                    elif current_attack == "attack_wait_2":
                        current_attack = "none"