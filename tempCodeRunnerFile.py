def btn_clicked(btn):
                    rect = getattr(btn, "rect", None)
                    if rect:
                        return rect.collidepoint((mx, my))
                    bx = getattr(btn, "x", getattr(btn, "pos_x", None))
                    by = getattr(btn, "y", getattr(btn, "pos_y", None))
                    img = getattr(btn, "img", getattr(btn, "image", None))
                    scale = getattr(btn, "scale", None)
                    if bx is None or by is None or img is None:
                        return False
                    w, h = img.get_width(), img.get_height()
                    if scale:
                        try:
                            w = int(w * scale); h = int(h * scale)
                        except Exception:
                            pass
                    return (bx <= mx <= bx + w) and (by <= my <= by + h)