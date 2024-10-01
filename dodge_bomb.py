import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP:(0,-5),
         pg.K_DOWN:(0,+5),
         pg.K_LEFT:(-5,0),
         pg.K_RIGHT:(+5,0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def game_over(screen, kk_rct):
    """ゲームオーバー時の画面を表示"""
    # 画面全体を黒で塗りつぶす
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.fill((0, 0, 0))
    blackout.set_alpha(150)  # 半透明にする
    screen.blit(blackout, (0, 0))

    # 泣いているこうかとんの画像を表示
    sad_kk_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    screen.blit(sad_kk_img, kk_rct)

    # Game Overの文字を表示
    font = pg.font.Font(None, 80)
    text = font.render("Game Over", True, (255, 0, 0))
    text_rct = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rct)

    # 画面更新
    pg.display.update()

    # 5秒間表示する
    time.sleep(5)

def create_bomb_lists():
    """爆弾の拡大と加速のリストを作成し、それらをタプルとして返す"""
    # 速度のリスト (1～10の加速度)
    accs = [a for a in range(1, 11)]
    
    # 爆弾サイズ（拡大したSurface）のリスト
    bb_imgs = []
    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))  # 爆弾のSurfaceを作成
        bb_img.set_colorkey((0, 0, 0))  # 背景を透過
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)  # 爆弾を描画
        bb_imgs.append(bb_img)
    
    return bb_imgs, accs

def update_bomb(tmr, vx, vy, bb_rct, bb_imgs, accs):
    """
    時間経過に応じて爆弾のサイズと速度を更新する。
    tmr: タイマーの値
    vx, vy: 爆弾の初期速度
    bb_rct: 爆弾のRect
    bb_imgs: 拡大爆弾Surfaceのリスト
    accs: 加速度のリスト
    """
    index = min(tmr // 100, 9)  # 最大で9を超えないようにする

    # 速度の更新
    avx = vx * accs[index]
    avy = vy * accs[index]
    # print(avx, avy)
    
    # 爆弾のサイズ更新
    bb_img = bb_imgs[index]
    bb_rct = bb_img.get_rect(center=bb_rct.center)  # 中心座標を維持したまま新しいサイズに更新
    
    return bb_img, avx, avy, bb_rct





def check_bound(obj_rct : pg.Rect) -> tuple[bool,bool]:
    """
    引数　こうかとん　または　爆弾のRect
    戻り値　真理値タプル（横判定結果、縦判定結果）
    画面内ならTrue、画面買いならFalse
    """
    yoko,tate = True,True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko,tate


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))  # 空のサーフェイス
    bb_img.set_colorkey((0,0,0))  # 爆弾の四隅の色を透過させる
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_rct = bb_img.get_rect()  # 爆弾レクトの抽出
    bb_lst,acc_lst = create_bomb_lists()
    bb_rct.centerx = random.randint(0,WIDTH)
    bb_rct.centery = random.randint(0,HEIGHT)
    vx,vy = +5,+5
    clock = pg.time.Clock()
    tmr = 0
    
    while True:
        b_img,ax,ay,b_rct = update_bomb(tmr,vx,vy,bb_rct,bb_lst,acc_lst)
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 

        if kk_rct.colliderect(b_rct):  # こうかとんと爆弾が重なっていたら
            game_over(screen, kk_rct)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key,tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True,True):
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])

        
        screen.blit(kk_img, kk_rct)

        
        bb_rct.move_ip(ax,ay)


        yoko,tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
            
        screen.blit(b_img, b_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
