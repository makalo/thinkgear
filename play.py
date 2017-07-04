# coding=UTF-8
#!/usr/bin/env python
import pygame,sys,time,random
from pygame.locals import *
import numpy as np
import win32api,win32con
import copy
import socket
import threading
blackColour = pygame.Color(0,0,0)
whiteColour = pygame.Color(255,255,255)
redColour = pygame.Color(255,0,0)
blueColour= pygame.Color(0,0,255)
yellowColour= pygame.Color(0,255,0)
bakColour=pygame.Color(50,50,50)

class game:
    def __init__(self,num,flag,tag):
        pygame.init()
        pygame.mixer.init()
        self.fpsClock = pygame.time.Clock()
        
        pygame.display.set_caption('脑电波对战人工智能')
        if flag==0:
            self.snakePosition_m = [140,240]
            self.snakeSegments_m = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction_m = 'right'
            if a==1:
                self.direction_m = 'left'
            if a==2:
                self.direction_m = 'up'
            if a==3:
                self.direction_m = 'down'
            self.changeDirection_m = self.direction_m

            self.snakePosition = [140,240]
            self.snakeSegments = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction = 'right'
            if a==1:
                self.direction = 'left'
            if a==2:
                self.direction = 'up'
            if a==3:
                self.direction = 'down'
            self.changeDirection = self.direction
            

            x = random.randrange(0,15)
            y = random.randrange(0,25)
            self.raspberryPosition = [int(x*20),int(y*20)]
            self.raspberrySpawned = 1
            
            self.fps=1
            self.temp=0
            self.con=8



        if num==1 and flag==1:
            self.snakePosition_m = [140,240]
            self.snakeSegments_m = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction_m = 'right'
            if a==1:
                self.direction_m = 'left'
            if a==2:
                self.direction_m = 'up'
            if a==3:
                self.direction_m = 'down'
            self.changeDirection_m = self.direction_m
            
        elif num==0 and flag==1:
            self.snakePosition = [140,240]
            self.snakeSegments = [[140,240]]
            a=random.randint(0,3)
            if a==0:
                self.direction = 'right'
            if a==1:
                self.direction = 'left'
            if a==2:
                self.direction = 'up'
            if a==3:
                self.direction = 'down'
            self.changeDirection = self.direction
            

        if tag==0:
            x = random.randrange(0,15)
            y = random.randrange(0,25)
            self.raspberryPosition = [int(x*20),int(y*20)]
            self.raspberrySpawned = 1
            self.playSurface = pygame.display.set_mode((500,500))
            
            
            # background = pygame.image.load('image/8.jpg').convert_alpha ()
            # width,height = background.get_size()
            # background = pygame.transform.smoothscale(background,(width//3,height//2))
            # self.playSurface.blit(background, (300,-20))




    def frame_step(self,input_actions,data,data_2,mutex,mutex2):
        #self.playSurface.set_clip(0,0, 300, 500)
        q=0
        acce=0
        terminal=False
        con=1
        image_data=np.zeros([300,500,3])
        feed_back=0

        #pygame.mixer.Sound('audio/swoosh.wav').play()
        #self.playSurface.set_clip(0,0, 300, 500)
        playSurface=self.playSurface.subsurface(pygame.rect.Rect((0,0), (300, 500)))
        lenth=len(data)
        if lenth==7:
            data1=data[6]
            data2=data[3]+data[4]+data[5]
            data3=data[0]+data[1]+data[2]
        elif lenth==6:
            data1=data[5]
            data2=data[2]+data[3]+data[4]
            data3=data[0]+data[1]
        elif lenth==1:
            data1=data[0]
            data2='0'
            data3='0'
        else:
            data1='0'
            data2='0'
            data3='0'

        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                # 判断键盘事件
                if event.key == ord('t'):
                    win32api.MessageBox(0,"切换到人工智能模式","提示",win32con.MB_OK)
                    self.temp=1
                if event.key == ord('f'):
                    win32api.MessageBox(0,"切换到对抗模式","提示",win32con.MB_OK)
                    self.temp=2
                if event.key == ord('c'):
                    win32api.MessageBox(0,"切换到人类玩家模式","提示",win32con.MB_OK)
                    self.temp=3
                if event.key == ord('0'):
                    feed_back=2
                    self.fps=1
                    win32api.MessageBox(0,"极简模式","提示",win32con.MB_OK)
                if event.key == ord('1'):
                    feed_back=2
                    self.fps=2
                    win32api.MessageBox(0,"简单模式","提示",win32con.MB_OK)
                if event.key == ord('2'):
                    feed_back=1
                    self.fps=4
                    win32api.MessageBox(0,"中级模式","提示",win32con.MB_OK)
                if event.key == ord('3'):
                    self.fps=10
                    win32api.MessageBox(0,"高级模式","提示",win32con.MB_OK)
                if event.key == ord('4'):
                    self.fps=30
                    win32api.MessageBox(0,"终极模式","提示",win32con.MB_OK)
                if event.key == ord('5'):
                    self.fps=80
                    win32api.MessageBox(0,"闪电蛇","提示",win32con.MB_OK)
                if event.key == ord('z'):
                    acce=1
                if event.key == K_RIGHT:
                    self.changeDirection_m = 'right'
                if event.key == K_LEFT:
                    self.changeDirection_m = 'left'
                if event.key == K_UP:
                    self.changeDirection_m = 'up'
                if event.key == K_DOWN:
                    self.changeDirection_m = 'down'
                if event.key == K_ESCAPE:
                    pygame.event.post(pygame.event.Event(QUIT))
        
        if self.direction_m=='right':
            # if data == '0':
            #     self.changeDirection_m = 'up'
            if data_2 == '1':
                self.changeDirection_m = 'down'
        if self.direction_m=='left':
            # if data == '0':
            #     self.changeDirection_m = 'down'
            if data_2 == '1':
                self.changeDirection_m = 'up'
        if self.direction_m=='up':
            # if data == '0':
            #     self.changeDirection_m = 'left'
            if data_2 == '1':
                self.changeDirection_m = 'right'
        if self.direction_m=='down':
            # if data == '0':
            #     self.changeDirection_m = 'right'
            if data_2 == '1':
                self.changeDirection_m = 'left'
        # print(data_2)
        # print (data)
        # print("kkkk")
        
        # if data == '0':
        #     self.changeDirection_m = 'right'
        # if data == '1':
        #     self.changeDirection_m = 'left'
        # if data == '2':
        #     self.changeDirection_m = 'up'
        # if data == '3':
        #     self.changeDirection_m = 'down'
        if data1=='4':
            self.temp=1
            #win32api.MessageBox(0,"切换到人工智能模式","提示",win32con.MB_OK)
        if data1=='5':
            self.temp=2
            #win32api.MessageBox(0,"切换到对抗模式","提示",win32con.MB_OK)
        if data1=='6':
            self.temp=3
            #win32api.MessageBox(0,"还原到最初模式","提示",win32con.MB_OK)
        if self.temp==0:
            self.temp=3
        
            # 判断是否输入了反方向

        if len(self.snakeSegments_m)!=1:
            if self.changeDirection_m == 'right' and not self.direction_m == 'left':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'left' and not self.direction_m == 'right':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'up' and not self.direction_m == 'down':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'down' and not self.direction_m == 'up':
                self.direction_m = self.changeDirection_m
        else:
            if self.changeDirection_m == 'right':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'left':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'up':
                self.direction_m = self.changeDirection_m
            if self.changeDirection_m == 'down':
                self.direction_m = self.changeDirection_m
        # 根据方向移动蛇头的坐标
        if self.temp==3 or self.temp==2:
            if self.direction_m == 'right':
                if acce==1:
                    self.snakePosition_m[0] += 40
                    for i in range(len(self.snakeSegments_m)):
                        self.snakeSegments_m[i][0]+=20
                else:
                    self.snakePosition_m[0] += 20
            if self.direction_m == 'left':
                if acce==1:
                    self.snakePosition_m[0] -= 40
                    for i in range(len(self.snakeSegments_m)):
                        self.snakeSegments_m[i][0]-=20
                else:
                    self.snakePosition_m[0] -= 20
                #self.snakePosition_m[0] -= 20
            if self.direction_m == 'up':
                if acce==1:
                    self.snakePosition_m[1] -= 40
                    for i in range(len(self.snakeSegments_m)):
                        self.snakeSegments_m[i][1]-=20
                else:
                    self.snakePosition_m[1] -= 20
                #self.snakePosition_m[1] -= 20
            if self.direction_m == 'down':
                if acce==1:
                    self.snakePosition_m[1] += 40
                    for i in range(len(self.snakeSegments_m)):
                        self.snakeSegments_m[i][1]+=20
                else:
                    self.snakePosition_m[1] += 20
                #self.snakePosition_m[1] += 20




        if self.temp==1 or self.temp==2:
            if sum(input_actions) != 1:
                raise ValueError('Multiple input actions!')

            if input_actions[0]==1:
                self.changeDirection = 'right'
            if input_actions[1]==1:
                self.changeDirection = 'left'
            if input_actions[2]==1:
                self.changeDirection = 'up'
            if input_actions[3]==1:
                self.changeDirection = 'down'

            if input_actions[0]==1 and not self.direction == 'left':
                self.direction = self.changeDirection
            if input_actions[1]==1 and not self.direction == 'right':
                self.direction = self.changeDirection
            if input_actions[2]==1 and not self.direction == 'down':
                self.direction = self.changeDirection
            if input_actions[3]==1 and not self.direction == 'up':
                self.direction = self.changeDirection
            # 根据方向移动蛇头的坐标
            if self.direction == 'right':
                self.snakePosition[0] += 20
                
            if self.direction == 'left':
                self.snakePosition[0] -= 20
             
            if self.direction == 'up':
                self.snakePosition[1] -= 20
               
            if self.direction == 'down':
                self.snakePosition[1] += 20
                
            # 增加蛇的长度
            self.snakeSegments.insert(0,list(self.snakePosition))
            
            # 判断是否吃掉了树莓
            if self.snakePosition[0] == self.raspberryPosition[0] and self.snakePosition[1] == self.raspberryPosition[1]:
                self.raspberrySpawned = 0
                pygame.mixer.Sound('audio/point.wav').play()
            else:
                self.snakeSegments.pop()
            # 如果吃掉树莓，则重新生成树莓
            if self.raspberrySpawned == 0:
                while(True):
                    x = random.randrange(0,15)
                    y = random.randrange(0,25)
                    self.raspberryPosition = [int(x*20),int(y*20)]
                    for position in self.snakeSegments:
                        if position==self.raspberryPosition:
                            q=1
                    if q==1:
                        q=0
                        continue
                    else:
                        break
                self.raspberrySpawned = 1
            q=0



         # 增加蛇的长度
        if self.temp==3 or self.temp==2:
            self.snakeSegments_m.insert(0,list(self.snakePosition_m))
            # 判断是否吃掉了树莓
            if self.snakePosition_m[0] == self.raspberryPosition[0] and self.snakePosition_m[1] == self.raspberryPosition[1]:
                self.raspberrySpawned = 0
                pygame.mixer.Sound('audio/point.wav').play()
            else:
                self.snakeSegments_m.pop()
            # 如果吃掉树莓，则重新生成树莓
            if self.raspberrySpawned == 0:
                while(True):
                    x = random.randrange(0,15)
                    y = random.randrange(0,25)
                    self.raspberryPosition = [int(x*20),int(y*20)]
                    for position in self.snakeSegments_m:
                        if position==self.raspberryPosition:
                            q=1
                    if q==1:
                        q=0
                        continue
                    else:
                        break
                self.raspberrySpawned = 1
            q=0





        
        if self.temp==1 or self.temp==2:
            #self.playSurface.fill(blackColour)
            #playSurface=self.playSurface.subsurface(pygame.rect.Rect((0,0), (300, 500)))
            #self.playSurface.subsurface(pygame.rect.Rect((0,0), (300, 500))).fill(blackColour)
            playSurface.fill(blackColour)
            for position in self.snakeSegments:
                pygame.draw.rect(playSurface,whiteColour,Rect(position[0],position[1],20,20))
                pygame.draw.rect(playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
            pygame.display.flip()
            
            #image_data = pygame.surfarray.array3d(pygame.display.get_surface())
            
            image_data = pygame.surfarray.array3d(self.playSurface.subsurface(pygame.rect.Rect((0,0), (300, 500))))
            #print (image_data.shape)
        
        if self.temp==1 or self.temp==2:
            if self.snakePosition[0] > 280 or self.snakePosition[0] < 0:
                terminal=True
                pygame.mixer.Sound('audio/hit.wav').play()
                if self.temp==1:
                    self.__init__(0,1,0)
                else:
                    self.__init__(0,1,1)
                
            if self.snakePosition[1] > 480 or self.snakePosition[1] < 0:
                terminal=True
                pygame.mixer.Sound('audio/hit.wav').play()
                if self.temp==1:
                    self.__init__(0,1,0)
                else:
                    self.__init__(0,1,1)


       
        # 绘制pygame显示层
        if self.temp==3 or self.temp==2:
            #self.playSurface.fill(blackColour)
            #self.playSurface.subsurface(pygame.rect.Rect((0,0), (300, 500))).fill(blackColour)
            playSurface.fill(blackColour)
            if self.temp==2:
                for position in self.snakeSegments:
                    pygame.draw.rect(playSurface,whiteColour,Rect(position[0],position[1],20,20))
                    pygame.draw.rect(playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))
            for position_m in self.snakeSegments_m:
                pygame.draw.rect(playSurface,blueColour,Rect(position_m[0],position_m[1],20,20))
                pygame.draw.rect(playSurface,redColour,Rect(self.raspberryPosition[0], self.raspberryPosition[1],20,20))

            # 刷新pygame显示层
            pygame.display.flip()
            # 判断是否死亡
            if self.snakePosition_m[0] > 280 or self.snakePosition_m[0] < 0:
                if self.temp==3:
                    self.__init__(1,1,0)
                else:
                    if terminal:
                        self.__init__(1,1,0)
                        pygame.mixer.Sound('audio/die.wav').play()
                    else:
                        self.__init__(1,1,1)
                    pygame.mixer.Sound('audio/die.wav').play()
            if self.snakePosition_m[1] > 480 or self.snakePosition_m[1] < 0:
                if self.temp==3:
                    self.__init__(1,1,0)
                else:
                    if terminal:
                        self.__init__(1,1,0)
                        pygame.mixer.Sound('audio/die.wav').play()
                    else:
                        self.__init__(1,1,1)
                        pygame.mixer.Sound('audio/die.wav').play()
        
        
        #pygame.display.update()
        self.playSurface.set_clip(300,0, 200, 500)
        self.playSurface.fill(bakColour)

        background0 = pygame.image.load('image/she2.jpg').convert_alpha ()
        background1 = pygame.image.load('image/ming3.jpg').convert_alpha ()
        background2 = pygame.image.load('image/zhuan3.jpg').convert_alpha ()
        background3 = pygame.image.load('image/zha.jpg').convert_alpha ()
        background4 = pygame.image.load('image/singal.jpg').convert_alpha ()
        background5 = pygame.image.load('image/zheng.jpg').convert_alpha ()
        background6 = pygame.image.load('image/ruo.jpg').convert_alpha ()
        background7 = pygame.image.load('image/lian.jpg').convert_alpha ()
        background8 = pygame.image.load('image/zhi.jpg').convert_alpha ()
        background9 = pygame.image.load('image/duan.jpg').convert_alpha ()
        background10 = pygame.image.load('image/mo.jpg').convert_alpha ()
        background11_1 = pygame.image.load('image/nao.jpg').convert_alpha ()
        background11_2 = pygame.image.load('image/nao_h.jpg').convert_alpha ()
        background12_1 = pygame.image.load('image/ren.jpg').convert_alpha ()
        background12_2 = pygame.image.load('image/ren_h.jpg').convert_alpha ()
        background13_1 = pygame.image.load('image/dui2.jpg').convert_alpha ()
        background13_2 = pygame.image.load('image/dui2_h.jpg').convert_alpha ()



        # width,height = background.get_size()
        # background = pygame.transform.smoothscale(background,(width,height))
        self.playSurface.blit(background0, (300,20))
        self.playSurface.blit(background1, (420,380))
        self.playSurface.blit(background2, (320,380))
        self.playSurface.blit(background3, (320,200))
        self.playSurface.blit(background4, (310,150))
        self.playSurface.blit(background7, (310,100))
        self.playSurface.blit(background10, (310,420))


        if self.temp==1:
            self.playSurface.blit(background12_2, (370,450))
            self.playSurface.blit(background11_1, (360,420))
            self.playSurface.blit(background13_1, (440,420))
        if self.temp==2:
            self.playSurface.blit(background12_1, (370,450))
            self.playSurface.blit(background11_1, (360,420))
            self.playSurface.blit(background13_2, (440,420))
        if self.temp==3:
            self.playSurface.blit(background12_1, (370,450))
            self.playSurface.blit(background11_2, (360,420))
            self.playSurface.blit(background13_1, (440,420))
        if data_2=='8':
            self.con=8
        if data_2=='9':
            self.con=9
        if self.con==8:
            self.playSurface.blit(background6, (400,150))
            self.playSurface.blit(background9, (400,100))
            
        if self.con==9:
            self.playSurface.blit(background5, (400,150))
            self.playSurface.blit(background8, (400,100))
            

        
        data1_1=int(data3)
        
        pygame.draw.rect(self.playSurface,redColour,Rect(340,350,20,-data1_1))#专注度
        data2_1=int(data2)
        pygame.draw.rect(self.playSurface,yellowColour,Rect(440,350,20,-data2_1))#冥想度
        if (data_2=='1'):
            pygame.draw.rect(self.playSurface,blueColour,Rect(440,200,20,20))
        else:
            pygame.draw.rect(self.playSurface,bakColour,Rect(440,200,20,20))

        pygame.display.flip()
        if data!='10':
            mutex.release()
        if data_2!='11':
            mutex2.release()
        self.fpsClock.tick(self.fps)

        return image_data,terminal,feed_back


