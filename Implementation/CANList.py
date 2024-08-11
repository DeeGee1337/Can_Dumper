from CANListNode import CANListNode


class CANList():
    def __init__(self):
        self.__list = []

    def insert_element(self, id, curr_occ, freq_time, freq_msg, curr_msg):
        # check if id is already existing
        if self.check_id(id):
            for node in self.__list:
                if node.check_id(id):
                    node.update(curr_occ=curr_occ, freq_time=freq_time, freq_msg=freq_msg, curr_msg=curr_msg)
        else:
            new_node = CANListNode(id=id, last_occ=0.0, curr_occ=curr_occ, frequency_time=freq_time, frequency_msg=freq_msg, 
                curr_msg=curr_msg, last_msg=None)
            self.__list.append(new_node)

    def check_id(self, id):
        id_exists = False
        for node in self.__list:
            if node.check_id(id):
                id_exists = True
        return id_exists

    def get_curr_occ(self, id):
        for node in self.__list:
            if node.check_id(id):
                return node.get_curr_occ()

    def print(self):
        for node in self.__list:
            node.print()
    
    def get_size(self):
        return len(self.__list)

    def get_can_node_by_id(self, id):
        for node in self.__list:
            if node.check_id(id):
                return node

