import sys
from base.enum import *
from ral_model.base import Base
from ral_model.field import Field

class Register(Base):
    def __init__(self, name):
        super().__init__(name)
        self.set_type(StorageType.REG)
        self.__field_list = []
        self.__rsv_cnt    = 0

    # ================ append field ================ #
    def append_field(self, field):
        if isinstance(field, Field):
            self.__field_list.append(field)
        else:
            print("[Error] invalid field object, please check!")
            sys.exit()

    def has_field(self, name):
        for f in self.__field_list:
            if f.get_name() == name:
                return True
        return False

    # ================ generate ralf code ================ #
    def gen_ralf_code(self):
        msb = 0
        ralf = f"register {self.get_name()} {{\n"
        for f in reversed(self.__field_list):
            ralf += f.gen_ralf_code()
            msb = f.get_bits()[0]

        msb = int(self.get_width()) - msb - 1
        if msb > 0:
            f_rsvd = Field("rsvd")
            f_rsvd.set_bits([int(self.get_width())-1, int(self.get_width())-msb])
            f_rsvd.set_access("ro")
            f_rsvd.set_reset(f"{msb}'h0")
            ralf += f_rsvd.gen_ralf_code()

        ralf += "}\n\n"
        return ralf
