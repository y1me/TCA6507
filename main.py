import EasyMCP2221
import time

class TCA6507(EasyMCP2221.Device):
    # Default I2C address for TCA6507
    TCA6507_ADDR = 0x45

    # TCA6507 NVM Register addresses
    Select0                 = 0x00
    Select1                 = 0x01
    Select2                 = 0x02
    FadeOn                  = 0x03
    FullyOn                 = 0x04
    FullyOff                = 0x05
    FirstFullyOff           = 0x06
    SecondFullyOff          = 0x07
    MaxIntensity            = 0x08
    ONESHOT                 = 0x09
    Initialization          = 0x0A
    Autoincrement           = 0x10

    NvmSize                 = 11

    LED_OFF                 = 0x00
    LED_ON_PWM0             = 0x02
    LED_ON_PWM1             = 0x03
    LED_FULLY_ON            = 0x04
    LED_ONE_SHOT            = 0x05
    LED_BLINK_0             = 0x06
    LED_BLINK_1             = 0x07

    MASK_SELECT0            = 0x01
    MASK_SELECT1            = 0x02
    MASK_SELECT2            = 0x04

    def __init__(self):
        # Initialize the parent class (EasyMCP2221.Device)
        super().__init__()
        self.HandleNotif = None
        self.LED = {
            "LED0": self.LED_OFF, #Green LED
            "LED1": self.LED_OFF, #Red LED
            "LED2": self.LED_OFF, #Blue LED
            "LED3": self.LED_OFF, #Button White LED
            "LED4": self.LED_OFF, #Logo White LED
            "LED5": self.LED_OFF,
            "LED6": self.LED_OFF
        }

        self.FadeONTime = {
            "BANK0": 9,
            "BANK1": 4
        }

        self.FullyONTime = {
            "BANK0": 6,
            "BANK1": 4
        }

        self.FadeOFFTime = {
            "BANK0": 9,
            "BANK1": 4
        }

        self.FullyOFFTime = {
            "BANK0": 8,
            "BANK1": 4
        }

        self.MaxIntensity = {
            "BANK0": 10,
            "BANK1": 10
        }

        self.OneShot = {
            "MasterIntensity": 15,
            "ALD_PWM0": 0,
            "ALD_PWM1": 0,
            "OneShotMode_PWM0": 0,
            "OneShotMode_PWM1": 0,
        }

        self.InitReg = {
            "BANK0": 15,
            "BANK1": 15
        }

    def scan(self):
        for addr in range(0, 0x80):
            try:
                self.I2C_read(addr)
                print("I2C slave found at address 0x%02X" % (addr))

            except EasyMCP2221.exceptions.NotAckError:
                pass

    def set_led(self,ledList,ledState):
        for x, y in self.LED.items():
            if x in ledList:
                self.LED[x] = ledState

    def set_oneshot_masterint_param(self,Param):
        self.tca6507_write([self.ONESHOT,((Param["ALD_INTENSITY"] & 0x0F) | (Param["ALD_EN_PWM0"] << 4 & 0x10) | (Param["ALD_EN_PWM1"] << 5 & 0x20) | (Param["ONE_SHOT_PWM0"] << 6 & 0x40) | (Param["ONE_SHOT_PWM1"] << 7 & 0x80))])
    def set_led_param(self,ledParam,Param):
        self.tca6507_write([ledParam,(Param["BANK1"] << 4 & 0xF0) | (Param["BANK0"] & 0x0F)])
    def tca6507_write(self,payload):
        self.I2C_write(addr=self.TCA6507_ADDR, data=bytes(payload))
    def tca6507_read(self, start_address,size):
        self.I2C_write(self.TCA6507_ADDR, [start_address], kind='nonstop')

        # Read max 100 bytes
        dataraw = self.I2C_read(addr=self.TCA6507_ADDR, size=size, kind='restart', timeout_ms=200)
        return dataraw

    def read_full_nvm(self):
        return self.tca6507_read(self.Select0 | self.Autoincrement, self.NvmSize)

    def update_led(self):
        # Read the NVM data
        dataSelect0 = 0x00
        dataSelect1 = 0x00
        dataSelect2 = 0x00
        for x, y in self.LED.items():
            match x:
                case "LED0":
                    print(y)
                    dataSelect0 |= ((y & self.MASK_SELECT0) >> 0) << 0
                    dataSelect1 |= ((y & self.MASK_SELECT1) >> 1) << 0
                    dataSelect2 |= ((y & self.MASK_SELECT2) >> 2) << 0
                case "LED1":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 1)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 1)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 1)
                case "LED2":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 2)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 2)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 2)
                case "LED3":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 3)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 3)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 3)
                case "LED4":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 4)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 4)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 4)
                case "LED5":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 5)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 5)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 5)
                case "LED6":
                    print(y)
                    dataSelect0 |= (((y & self.MASK_SELECT0) >> 0) << 6)
                    dataSelect1 |= (((y & self.MASK_SELECT1) >> 1) << 6)
                    dataSelect2 |= (((y & self.MASK_SELECT2) >> 2) << 6)
        self.tca6507_write([self.Select0 | self.Autoincrement, dataSelect0, dataSelect1, dataSelect2])



def main():
    LED_OFF                 = 0x00
    LED_ON_PWM0             = 0x02
    LED_ON_PWM1             = 0x03
    LED_FULLY_ON            = 0x04
    LED_ONE_SHOT            = 0x05
    LED_BLINK_0             = 0x06
    LED_BLINK_1             = 0x07

    FADEON = 0x03
    FULLYON = 0x04
    FADEOFF = 0x05
    FIRSTFULLYOFF = 0x06
    SECONDFULLYOFF = 0x07
    MAXINTENSITY = 0x08
    ONESHOT = 0x09
    INITIALIZATION = 0x0A
    AUTOINCREMENT = 0x10

    tca6507 = TCA6507()

    tca6507.scan()

    #Set All LED OFF
    tca6507.set_led(["LED0","LED1","LED2","LED5","LED6","LED7"],LED_OFF)
    tca6507.set_led(["LED3","LED4"],LED_OFF)
    # write 0xOO in reg 0x00, 0x01, 0x02
    tca6507.update_led()
################# POWER ON/OFF CONFIG #########################################
    #Power on/off config (WHITE LED FADE ON/FADE OFF)
    # write 0xCA in reg 0x09
    tca6507.set_oneshot_masterint_param({"ALD_INTENSITY":10,"ALD_EN_PWM0":0,"ALD_EN_PWM1":0,"ONE_SHOT_PWM0":1,"ONE_SHOT_PWM1":1})
    # write 0xOO in reg 0x10
    tca6507.set_led_param(INITIALIZATION,{"BANK0":0,"BANK1":0})
    # write 0xAA in reg 0x04
    tca6507.set_led_param(FULLYON,{"BANK0":10,"BANK1":10})
    # write 0xAA in reg 0x06
    tca6507.set_led_param(FIRSTFULLYOFF,{"BANK0":10,"BANK1":10})
    # write 0xAA in reg 0x07
    tca6507.set_led_param(SECONDFULLYOFF,{"BANK0":10,"BANK1":10})
    # write 0xAA in reg 0x03
    tca6507.set_led_param(FADEON,{"BANK0":13,"BANK1":13})
    # write 0xAA in reg 0x05
    tca6507.set_led_param(FADEOFF,{"BANK0":13,"BANK1":13})
    # write 0xAA in reg 0x08
    tca6507.set_led_param(MAXINTENSITY,{"BANK0":15,"BANK1":15})

    tca6507.set_led(["LED3","LED4"],LED_BLINK_1)

    #Trigger White LED power on with FadeOn
    tca6507.set_led_param(FADEON,{"BANK0":13,"BANK1":13})
    tca6507.set_led_param(INITIALIZATION,{"BANK0":10,"BANK1":12})
    #Set bit 3,4 in register 0x00, 0x01 and 0x02
    tca6507.update_led()

    # Debug Print ALL
    #Led power on done when bit 3,4 set in 0x00 and 0x01 register and bit 3,4 reset in 0x02 register
    data = tca6507.read_full_nvm()
    listo = data.hex()
    n = 2
    datalist = [listo[i:i + n] for i in range(0, len(listo), n)]
    print(datalist)

    #Setup White LED power off with FadeOff
    tca6507.set_led(["LED0","LED1","LED2","LED5","LED6","LED7"],LED_OFF)
    tca6507.set_led(["LED3","LED4"],LED_BLINK_0)

    #Trigger White LED power on with FadeOFF
    tca6507.set_led_param(FADEOFF,{"BANK0":13,"BANK1":13})
    tca6507.set_led_param(INITIALIZATION,{"BANK0":10,"BANK1":12})
    #Set bit 3,4 in register 0x01 and 0x02, reset bit 3,4 in register 0x00
    tca6507.update_led()

    # Debug Print ALL
    #Led power off done when bit 3,4 reset in 0x00, 0x01 and 0x02 register
    data = tca6507.read_full_nvm()
    listo = data.hex()
    n = 2
    datalist = [listo[i:i + n] for i in range(0, len(listo), n)]
    print(datalist)

    ################# BATTERY POWERED DEVICE #########################################

    tca6507.set_oneshot_masterint_param({"ALD_INTENSITY": 15, "ALD_EN_PWM0": 0, "ALD_EN_PWM1": 0, "ONE_SHOT_PWM0": 0, "ONE_SHOT_PWM1": 0})
    tca6507.set_led_param(FULLYON, {"BANK0": 2, "BANK1": 2})
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 3, "BANK1": 4})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 10, "BANK1": 4})
    tca6507.set_led_param(FADEON, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led_param(FADEOFF, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led_param(MAXINTENSITY, {"BANK0": 15, "BANK1": 15})
    #Set bit 3,4 in register 0x01, reset bit 3,4 in register 0x00 and 0x02
    tca6507.set_led(["LED3", "LED4"], LED_ON_PWM0)
    tca6507.set_led(["LED0", "LED2", "LED5", "LED6", "LED7"], LED_OFF)


    # Low Bat ON
    tca6507.set_led(["LED1"], LED_BLINK_0)
    tca6507.update_led()

    # Low Bat OFF
    tca6507.set_led(["LED1"], LED_OFF)
    tca6507.update_led()


    # BLE connectable ON
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 3, "BANK1": 4})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 10, "BANK1": 4})
    tca6507.set_led_param(FADEON, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led_param(FADEOFF, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led(["LED2"], LED_BLINK_1)
    tca6507.update_led()

    # BLE connectable OFF
    tca6507.set_led(["LED2"], LED_OFF)
    tca6507.update_led()

    # BLE connected ON
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 3, "BANK1": 12})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 10, "BANK1": 12})
    tca6507.set_led_param(FADEON, {"BANK0": 2, "BANK1": 8})
    tca6507.set_led_param(FADEOFF, {"BANK0": 2, "BANK1": 8})
    tca6507.set_led(["LED2"], LED_BLINK_1)
    tca6507.update_led()

    # BLE connected OFF
    tca6507.set_led(["LED2"], LED_OFF)
    tca6507.update_led()


    ################# USB POWERED DEVICE #########################################

    tca6507.set_oneshot_masterint_param({"ALD_INTENSITY": 15, "ALD_EN_PWM0": 0, "ALD_EN_PWM1": 0, "ONE_SHOT_PWM0": 0, "ONE_SHOT_PWM1": 0})
    tca6507.set_led_param(FULLYON, {"BANK0": 6, "BANK1": 2})
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 4, "BANK1": 4})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 4, "BANK1": 4})
    tca6507.set_led_param(FADEON, {"BANK0": 9, "BANK1": 1})
    tca6507.set_led_param(FADEOFF, {"BANK0": 9, "BANK1": 1})
    tca6507.set_led_param(MAXINTENSITY, {"BANK0": 15, "BANK1": 15})
    tca6507.set_led(["LED3", "LED4"], LED_ON_PWM0)
    tca6507.set_led(["LED1", "LED2", "LED5", "LED6", "LED7"], LED_OFF)


    #Charge LED Battery is charging
    tca6507.set_led(["LED0"], LED_BLINK_0)
    tca6507.update_led()

    #Charge LED Battery charged
    tca6507.set_led(["LED0"], LED_ON_PWM0)
    tca6507.update_led()

    #Charge LED OFF
    tca6507.set_led(["LED0"], LED_OFF)
    tca6507.update_led()


    # BLE connectable ON
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 3, "BANK1": 4})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 10, "BANK1": 4})
    tca6507.set_led_param(FADEON, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led_param(FADEOFF, {"BANK0": 2, "BANK1": 1})
    tca6507.set_led(["LED2"], LED_BLINK_1)
    tca6507.update_led()

    # BLE connectable OFF
    tca6507.set_led(["LED2"], LED_OFF)
    tca6507.update_led()

    # BLE connectable ON
    tca6507.set_led_param(FIRSTFULLYOFF, {"BANK0": 3, "BANK1": 12})
    tca6507.set_led_param(SECONDFULLYOFF, {"BANK0": 10, "BANK1": 12})
    tca6507.set_led_param(FADEON, {"BANK0": 2, "BANK1": 8})
    tca6507.set_led_param(FADEOFF, {"BANK0": 2, "BANK1": 8})
    tca6507.set_led(["LED2"], LED_BLINK_1)
    tca6507.update_led()

    # BLE connectable OFF
    tca6507.set_led(["LED2"], LED_OFF)
    tca6507.update_led()


# Print ALL
    data=tca6507.read_full_nvm()
    listo = data.hex()
    n = 2
    datalist = [listo[i:i + n] for i in range(0, len(listo), n)]
    print(datalist)

if __name__ == "__main__":
    main()


