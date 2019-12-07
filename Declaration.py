class Road:
    def __init__(self, city, numOfCell=10, introRate=2, remvRate=2, carRateDist = {}, direction = (0,1),moveProb=0.5, startPos = (0,0),interval =0.001,totalTime = 1000,name=''):
        #int numOfCell, int introRate, int remvRate, int index
        self.__introRate = introRate
        self.__remvRate = remvRate
        self.carRateDist = carRateDist 
        self.allCars = [] #cars in this road
        self.numOfCell = numOfCell
        self.passCar = 0 # number of the passing cars
        self.conflict = 0
        self.direction = direction
        self.startPos = startPos
        self.endPos = (startPos[0]+self.direction[0]*(self.numOfCell-1), startPos[1]+self.direction[1]*(self.numOfCell-1))
        #self.cell = {}  #cells in this road
        self.city = city
        self.time_sum_car = 0
        self.density = 0
        self.J = 0
        self.interval = interval
        self.totalTime = totalTime
        self.name = name
        self.moveProb = moveProb
        
        ###################################################################
        self.cells = []
        for i in range(self.numOfCell):
            self.cells.append((self.startPos[0]+self.direction[0]*i, self.startPos[1]+self.direction[1]*i))
        
        for point in self.cells:
            if point in self.city.map:
                if self.city.map[point] == 1:
                    for road in self.city.roads:
                        if point in road.cells:
                            self.city.crossRoad.update({point:(road, self)})
            else:
                self.city.map[point] = 1
        ##################################################################
        
        #for i in range(self.numOfCell):
            #self.city.map[(self.startPos[0]+self.direction[0]*i, self.startPos[1]+self.direction[1]*i)] = 1
        
    def introCar(self):
        # introduce a new car to this road
        if ((random.random() < self.__introRate*self.interval) and(self.city.map[self.startPos] == 1)):
            self.city.map[self.startPos] = 2
            carRate = abs(np.random.normal(self.carRateDist['mean'],self.carRateDist['var']**(0.5)))
            newCar = Car(self, prob=self.moveProb, interval = self.interval,expClockRate= carRate)
            #self.allCars.insert(0, newCar)
            self.allCars.append(newCar)
            
    def remvCar(self):
        # remove the car in the last cell of this road
        if ((random.random() < self.__remvRate*self.interval)and (self.city.map[self.endPos] == 2)):
            self.city.map[self.endPos] = 1
            self.allCars.pop(0)
            self.passCar += 1
            
    def showCar(self):
        for i in range(self.numOfCell):
            if self.city.map[(self.startPos[0]+self.direction[0]*i, self.startPos[1]+self.direction[1]*i)] == 1:
                print(" | "+" ",end="")
            else:
                print(" | "+"*",end="")
        print(" |\n")
    def calculateRate(self):
        self.density = self.time_sum_car/(self.totalTime/self.interval*self.numOfCell)
        self.J = self.passCar / self.totalTime
        


class Car:
    def __init__(self, road, position=0, expClockRate=3, prob=0.5,interval =0.001):
        #int position, int expClockRate, float prob, int index (which road)
        self.__position = (road.startPos[0]+road.direction[0]*position, road.startPos[1]+road.direction[1]*position)
        self.__expClockRate = expClockRate
        self.__prob = prob
        self.__road = road
        self.accident = 0
        self.interval = interval
    def moveForward(self):
        if(self.__position==self.__road.endPos):
            return "end"
        if (random.random() < self.__expClockRate*self.interval) and (random.random() < self.__prob):
            # expo & not broken
            if (self.__road.city.map[(self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])] == 1): # next cell is empty
                self.__road.city.map[self.__position] = 1
                self.__position = (self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])
                self.__road.city.map[self.__position] = 2
            elif(self.__road.city.map[(self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])] == 4) and \
            self.__road.city.map[(self.__position[0]+self.__road.direction[0]*2, self.__position[1]+self.__road.direction[1]*2)] == 1:#green light
                self.__road.city.map[self.__position] = 1
                self.__position = (self.__position[0]+self.__road.direction[0]*2, self.__position[1]+self.__road.direction[1]*2)
                self.__road.city.map[self.__position] = 2
            else:
                return "conflict"
                
        return "move"
    ##################################################################
    def moveForwardWithCRA(self):
        if(self.__position == self.__road.endPos):
            return "end"
        if (random.random() < self.__expClockRate*self.interval) and (random.random() < self.__prob)and (self.accident == 0):
            # expo & not broken
            if self.__position in self.__road.city.crossRoad:
                self.__road.allCars.pop(self.__road.allCars.index(self))
                if random.random() > 0.5:
                    self.__road = self.__road.city.crossRoad[self.__position][0]
                else:
                    self.__road = self.__road.city.crossRoad[self.__position][1]
                for car in self.__road.allCars:
                    if self.__road.direction > (0,0):
                        if self.__position > car.__position:
                            self.__road.allCars.insert(self.__road.allCars.index(car), self)
                            break
                    else:
                        if self.__position < car.__position:
                            self.__road.allCars.insert(self.__road.allCars.index(car), self)
                            break
                    
                    
############################ move ###############################            

            
            if (self.__road.city.map[(self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])] == 1): # next cell is empty
                self.__road.city.map[self.__position] = 1
                self.__position = (self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])
                self.__road.city.map[self.__position] = 2
            elif(self.__road.city.map[(self.__position[0]+self.__road.direction[0], self.__position[1]+self.__road.direction[1])] == 4) and \
            self.__road.city.map[(self.__position[0]+self.__road.direction[0]*2, self.__position[1]+self.__road.direction[1]*2)] == 1:#green light
                self.__road.city.map[self.__position] = 1
                self.__position = (self.__position[0]+self.__road.direction[0]*2, self.__position[1]+self.__road.direction[1]*2)
                self.__road.city.map[self.__position] = 2
            else:
                return "conflict"
############################ move ###############################            
            
            
            if ((self.__position[0]+2*self.__road.direction[0], self.__position[1]+2*self.__road.direction[1]) in self.__road.city.crossRoad) \
            or ((self.__position[0]-self.__road.direction[0], self.__position[1]-self.__road.direction[1]) in self.__road.city.crossRoad) \
            or ((self.__position[0]-2*self.__road.direction[0], self.__position[1]-2*self.__road.direction[1]) in self.__road.city.crossRoad):
                self.__road.city.map[self.__position] = 10
            if self.__position in self.__road.city.crossRoad:
                self.__road.city.map[self.__position] = 10
            return "move"
        
        elif (self.accident == 1):
            self.__road.city.map[self.__position] = 20

    ##################################################################

class City:
    def __init__(self, acciProb=0.05,l=100, w=100,totalTime = 1000,interval = 0.001,name='Berkeley'):
        self.l = l
        self.w = w
        self.map = {(i,j):0 for i in range(-self.l,-self.l) for j in range(-self.w,self.w)} 
        self.roads=[]
        self.totalTime = totalTime
        self.interval = interval
        self.name = name
        self.J = 0
        self.density = 0
        self.time_sum_car = 0
        self.numOfCell = 0
        self.passCar = 0
        self.acciProb = acciProb
        
        
        ##################################################################
        self.crossRoad = {}
        self.accCars = []
        ##################################################################

    def showCity(self):
        rx, ry = [],[]
        cx, cy = [],[]
        lx, ly = [],[]
        gx, gy = [],[]
        crx, cry = [],[]
        accx = []
        accy = []
        for i in self.map:
            if self.map[i] != 0:
                rx.append(i[0])
                ry.append(i[1])
            if self.map[i] == 2:
                cx.append(i[0])
                cy.append(i[1])
            elif self.map[i] == 3:
                lx.append(i[0])
                ly.append(i[1])
            elif self.map[i] == 4:
                gx.append(i[0])
                gy.append(i[1])
            elif self.map[i] == 10:
                crx.append(i[0])
                cry.append(i[1])
            elif self.map[i] == 20:
                accx.append(i[0])
                accy.append(i[1])
                
            
        plt.plot(rx, ry, marker="o",color="navy",linestyle=" ",markersize=2)
        plt.plot(cx, cy, marker="*",color="y",linestyle=" ")
        plt.plot(lx, ly, marker="s",color="r",linestyle=" ")
        plt.plot(gx, gy, marker="s",color="lightgreen",linestyle=" ")
        plt.plot(crx, cry, marker="H",color="orange",linestyle=" ")
        ax.plot(accx, accy, marker="x",color="pink",linestyle=" ")
        plt.show()
        
    def showCitySub(self):
        ax.clear()
        rx = []
        ry = []
        cx = []
        cy = []
        lx = []
        ly = []
        gx = []
        gy = []
        crx = []
        cry = []
        accx = []
        accy = []
        for i in self.map:
            if self.map[i] != 0:
                rx.append(i[0])
                ry.append(i[1])
            if self.map[i] == 2:
                cx.append(i[0])
                cy.append(i[1])
            elif self.map[i] == 3:
                lx.append(i[0])
                ly.append(i[1])
            elif self.map[i] == 4:
                gx.append(i[0])
                gy.append(i[1])
            elif self.map[i] == 10:
                crx.append(i[0])
                cry.append(i[1])
            elif self.map[i] == 20:
                accx.append(i[0])
                accy.append(i[1])
        ax.plot(rx, ry, marker="o",color="navy",linestyle=" ",markersize=8)
        ax.plot(cx, cy, marker="*",color="y",linestyle=" ")
        ax.plot(lx, ly, marker="s",color="r",linestyle=" ")
        ax.plot(gx, gy, marker="s",color="lightgreen",linestyle=" ")
        ax.plot(crx, cry, marker="h",color="orange",linestyle=" ")
        ax.plot(accx, accy, marker="x",color="pink",linestyle=" ")
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.title("Map")
        fig.canvas.draw()
    
    def createRoad(self,numOfCell=10, introRate=2, remvRate=2,carRate = {'mean':5,'var':2},moveProb=0.5, direction = (0,1), startPos = (0,0),name = ''):
        newRoad = Road(self, numOfCell=numOfCell, introRate=introRate, remvRate=remvRate, direction = direction, \
                       startPos = startPos,moveProb=moveProb,carRateDist =carRate, interval = self.interval,totalTime = self.totalTime, name = name)
        self.roads.append(newRoad)
        self.numOfCell += newRoad.numOfCell
    def introCar(self):
        for road in self.roads:
            road.introCar()
            
    def remvCar(self):
        self.passCar = 0
        for road in self.roads:
            road.remvCar()
            self.passCar += road.passCar
    def moveCar(self):
        for road in self.roads:
            for car in road.allCars:
                ret = car.moveForward()
                if ret =="conflict":
                    road.conflict += 1
                    
    ##################################################################               
    def moveCarWithCRA(self):
        for road in self.roads:
            for car in road.allCars:
                ret = car.moveForwardWithCRA()
                if ret =="conflict":
                    road.conflict += 1
                    
        if random.random() < self.acciProb:
            accRoad = random.choice(self.roads)
            if accRoad.allCars != []:
                accCar = random.choice(accRoad.allCars)
                self.accCars.append(accCar)
                accCar.accident = 1
            
        if (random.random() < 0.3) and (self.accCars != []):
            fixCar = random.choice(self.accCars)
            self.accCars.pop(self.accCars.index(fixCar))
            fixCar.accident = 0
    ##################################################################
                    
    
    def Time_sum_car(self):
        for road in self.roads:
            road.time_sum_car += len(road.allCars)
    def calculateRate(self):
        self.time_sum_car=0
        for road in self.roads:
            road.calculateRate()
            self.time_sum_car += road.time_sum_car
        self.density = self.time_sum_car/(self.totalTime/self.interval*self.numOfCell)
        self.J = self.passCar / self.totalTime
    def light(self, position):
        if random.random < 0.5:
            self.City.map[position] = 3
        else:
            self.City.map[position] = 1
            
    def crossRoadLight(self, position1, position2):
        if random.random() < 0.5:
            self.map[position1] = 3
            self.map[position2] = 1
        else:
            self.map[position1] = 1
            self.map[position2] = 3
            
    def crossRoadLight2(self, position1, position2, position3, position4, counter): #1=3, 2=4
        if(counter % 50 <= 24):
            self.map[position1] = 3
            self.map[position2] = 4
            self.map[position3] = 3
            self.map[position4] = 4
        else:
            self.map[position1] = 4
            self.map[position2] = 3
            self.map[position3] = 4
            self.map[position4] = 3
    def freshMap(self):
        del(self.roads[:])
        self.numOfCell = 0
        self.roads=[]
        
        ##################################################################
        self.crossRoad = {}
        ##################################################################


        #self.map = {i:0 for i in self.map}
        self.map={}

