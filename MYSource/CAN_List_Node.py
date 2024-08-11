

class CANListNode():
    def __init__(self, id, last_occ, curr_occ, frequency_time, frequency_msg, curr_msg, last_msg):
        self.__id = id
        self.__last_occ = last_occ
        self.__curr_occ = curr_occ
        self.__frequency_time = frequency_time
        self.__frequency_msg = frequency_msg
        self.__curr_msg = curr_msg
        self.__last_msg = last_msg

    def update(self, curr_occ, freq_time, freq_msg, curr_msg):
        self.__last_occ = self.__curr_occ
        self.__curr_occ = curr_occ
        self.__frequency_time = freq_time
        self.__frequency_msg = freq_msg
        self.__last_msg = self.__curr_msg
        self.__curr_msg = curr_msg

    def check_id(self, id):
        if id == self.__id:
            return True
        else:
            self.set_freq_msg(self.get_freq_msg() + 1)
            return False
    
    def print(self):
        print(str(self.__id) + ': ' + str(self.__curr_occ) + ' - ' + str(self.__last_occ) + ' = ' + str(self.__frequency_time))

    def get_id(self):
        return self.__id

    def get_last_occ(self):
        return self.__last_occ

    def get_curr_occ(self):
        return self.__curr_occ

    def get_freq_time(self):
        return self.__frequency_time

    def get_freq_msg(self):
        return self.__frequency_msg

    def get_curr_msg(self):
        return self.__curr_msg
    
    def get_last_msg(self):
        return self.__last_msg
        
    def set_id(self, id):
        self.__id = id

    def set_last_occ(self, new_last_occ):
        self.__last_occ = new_last_occ
        
    def set_curr_occ(self, new_curr_occ):
        self.__curr_occ = new_curr_occ

    def set_freq_time(self, new_freq_time):
        self.__frequency_time = new_freq_time

    def set_freq_msg(self, new_freq_msg):
        self.__frequency_msg = new_freq_msg

    def set_curr_msg(self, new_curr_msg):
        self.__curr_msg = new_curr_msg

    def reset_freq_msg(self):
        self.set_freq_msg(0)