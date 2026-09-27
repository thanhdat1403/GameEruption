import math
import random
import pygame
import numpy as np

class Ball:
    def __init__(self, position, velocity): #vị trí và tốc độ quả bóng
        self.pos = np.array(position, dtype=np.float64)
        self.v = np.array(velocity, dtype=np.float64)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))#tạo ra quả bóng ngẫu nhiên ,với màu ngẫu nhiên
        self.is_in = True # mỗi quả bóng ở trong tình trạng ở trong

#hàm kiểm tra quả bóng có ở trong dây cung hay không
def is_ball_in_arc(ball_pos, CIRCLE_CENTER, start_angle, end_angle):
    dx = ball_pos[0] - CIRCLE_CENTER[0]
    dy = ball_pos[1] - CIRCLE_CENTER[1]
    ball_angle = math.atan2(dy, dx) # góc của quả bóng, math.atan2(dy, dx): là lấy ngược lại của cái tan
    start_angle = start_angle % (2 * math.pi)#quy lại góc về giá trị từ 0-2pi
    end_angle = end_angle % (2 * math.pi)#quy lại góc về giá trị từ 0-2pi
    if start_angle > end_angle:
        end_angle += 2 * math.pi
    if start_angle <= ball_angle <= end_angle or (start_angle <= ball_angle + 2 * math.pi <= end_angle):# kiểm tra quả bóng đấy có ở giữa góc bắt đầu và góc cuối k và check cái góc của quả bóng +2pi cũng ở cái khoảng bắt đầu đến kết thúc
        return True

#hàm để vẽ tam giác đâm từ đỉnh tam giác vào tâm đường tròn để tạo chỗ khuyết
def draw_arc(window, center,radius, start_angle, end_angle): # draw_arc là vẽ dây cung nhưng thật ra là vẽ tam giác đè nên và có: tâm đường tròn, bán kính, góc bắt đầu, góc kết thúc
    p1 = center + (radius + 1000) * np.array([math.cos(start_angle), math.sin(start_angle)]) # điểm bắt đầu
    p2 = center + (radius + 1000) * np.array([math.cos(end_angle), math.sin(end_angle)]) # điểm kết thúc
    pygame.draw.polygon(window,BLACK, [center,p1,p2], 0) #pygame.draw.polygon hàm này thức chất là vẽ ra tam giác được tạo bởi 3 điểm

pygame.init()
WIDTH = 800
HEIGHT = 800
window = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)
CIRCLE_CENTER = np.array([WIDTH/2, HEIGHT/2], dtype=np.float64) # tọa độ tâm đường tròn
CIRCLE_RADIUS = 150 #bán kính đường tròn màu cam
BALL_RADIUS = 5#bán kính của quả bóng màu đỏ
ball_pos = np.array([WIDTH/2, HEIGHT/2 - 120], dtype=np.float64) #tọa độ của quả bóng đầu tiên(tâm quả bóng)
running = True
GRAVITY = 0.2
ball_vel = np.array([0,0], dtype=np.float64)# vận tốc của quả bóng và vận tốc ban đầu là (0,0)
arc_degrees = 60 # độ của dây cung, góc khuyết là 60 độ
start_angle = math.radians(-arc_degrees / 2) # góc bắt đầu và cái hàm math.radians có tác dụng là đổi tử độ sang rad
end_angle = math.radians(arc_degrees / 2) # góc kết thúc là cái góc đấy = 60/2 và cái hàm math.radians có tác dụng là đổi tử độ sang rad
spinning_speed = 0.01 #tốc độ quay
balls = [Ball(ball_pos, ball_vel)]
#vòng lặp game
while running:
    #3 dòng này để sử lý nút bấm(Vòng nặp game)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    start_angle += spinning_speed
    end_angle += spinning_speed
    for ball in balls:# nặp qua từng quả bóng trong danh sách những quả bóng
        if ball.pos[1] > HEIGHT or ball.pos[0]<0 or ball.pos[0]>WIDTH or ball.pos[1]<0:#nếu vị trí y lớn hơn chiều cao và vị trí x < 0 , ball.pos[0]>WIDTH or ball.pos[1]<0(kiểm tra quả bóng có đi ra ngoài hay không)
            balls.remove(ball) # nếu đi ra ngoài thì xóa
            # và tạo 2 quả bóng ngẫu nhiên
            balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4),random.uniform(-1, 1)]))
            balls.append(Ball(position=[WIDTH // 2, HEIGHT // 2 - 120], velocity=[random.uniform(-4, 4),random.uniform(-1, 1)]))

        ball.v[1] = ball.v[1] + GRAVITY
        ball.pos += ball.v # cập nhật x,y (vì là numpy array mới đc làm cái này)
        #khoảng cách dist
        dist = np.linalg.norm(ball.pos - CIRCLE_CENTER)
        if dist + BALL_RADIUS > CIRCLE_RADIUS: # Nếu khoảng cách của quả bóng lớn hơn bán kính đường tròn màu cam thì nghĩa là quả bóng ra ngoài(Hay là dòng này kiểm tra quả bóng chạm vào đường tròn)
            if is_ball_in_arc(ball.pos, CIRCLE_CENTER, start_angle, end_angle):# khi check nó chạm vào rồi ở if trên thì ktra xem nó có ở giữa 2 cái góc start_angle và end_angle ở cái khoảng khuyết hay k
                ball.is_in = False # nếu nó chạm vào khoảng khuyết nghĩa là quả bóng đó đã rơi ra ngoài
            if ball.is_in == True:#nghĩa là quả bóng ở bên trong thì mới cho nó lẩy
                #BƯỚC 1: Tính vecto d (là vecto nối từ tâm đường tròn cam đến tiếp tuyến t)
                d = ball.pos - CIRCLE_CENTER
                d_unit = d/np.linalg.norm(d) # vecto đơn vị d
                #Cập nhập vị trí quả bóng để quả bóng chạm vào đường tròn mà vẫn bên trong(lẩy bên trong)
                ball.pos = CIRCLE_CENTER + (CIRCLE_RADIUS - BALL_RADIUS) * d_unit #tâm đường tròn + (bán kính đường tròn - bán kính của quả bóng) * vecto đơn vị
                #BƯỚC 2: Tính tiếp tuyến t
                t = np.array([-d[1],d[0]], dtype=np.float64)#-d[1] là -y còn d[0] là x
                #BƯỚC 3:Tính hình chiếu từ vecto t đến vecto v
                proj_v_t = (np.dot(ball.v,t)/np.dot(t,t)) * t #dùng hàm này để tính tích vô hướng(np.dot())
                ball.v = 2 * proj_v_t - ball.v
                ball.v += t * spinning_speed #câu lệnh này có tác dụng tạo ra lực kéo và có ct: v = rw(w chính là tốc độ quay spinning_speed,r là bán kính)
    window.fill(BLACK)#cho toàn bộ màn hình màu đen
    pygame.draw.circle(window, ORANGE, CIRCLE_CENTER, CIRCLE_RADIUS, 3)# hàm để vẽ 1 đường tròn màu cam
    draw_arc(window, CIRCLE_CENTER, CIRCLE_RADIUS, start_angle, end_angle)
    for ball in balls:# vòng lặp để vẽ quả bóng
        pygame.draw.circle(window, ball.color, ball.pos, BALL_RADIUS)#vẽ quả bóng màu đỏ
    pygame.display.flip()
    clock.tick(60) #1s chạy 60 lần

pygame.quit()