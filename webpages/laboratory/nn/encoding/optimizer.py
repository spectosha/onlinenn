from keras.optimizers import Adam, SGD, RMSprop, Adadelta, Adagrad, Adamax


class Optimizer:

    fields = None
    opt = None

    def __init__(self, list, get_from):
        self.opt = list["name"]
        self.fields = list["fields"]

    def get_opt(self):
        opt = self.opt
        if opt == "Adam":
            return Adam(lr = self.get_float("lr"),
                        beta_1 = self.get_float("beta_1"),
                        beta_2=self.get_float("beta_2"),
                        epsilon=self.get_float("epsilon"),
                        decay=self.get_float("decay"),
                        amsgrad=self.get_bool("decay"),)
        elif opt == "Adamax":
            return Adamax(lr = self.get_float("lr"),
                        beta_1 = self.get_float("beta_1"),
                        beta_2=self.get_float("beta_2"),
                        epsilon=self.get_float("epsilon"),
                        decay=self.get_float("decay"),)
        elif opt == "SGD":
            return SGD(lr = self.get_float("lr"),
                       momentum = self.get_float("momentum"),
                       decay=self.get_float("decay"))
        elif opt == "RMSprop":
            return RMSprop(lr = self.get_float("lr"),
                           rho = self.get_float("rho"),
                           decay=self.get_float("decay"),
                           epsilon = self.get_float("epsilon"),)
        elif opt == "Adagrad":
            return Adagrad(lr = self.get_float("lr"),
                           epsilon = self.get_float("epsilon"),
                           decay=self.get_float("decay"))
        elif opt == "Adadelta":
            return Adadelta(lr = self.get_float("lr"),
                            rho = self.get_float("rho"),
                            epsilon = self.get_float("epsilon"),
                            decay=self.get_float("decay"))
        return "adam"

    def get_float(self, value):
        i = 0
        while i < len(self.fields):
            if self.fields[i]["name"] == value:
                if self.fields[i]["value"] == "None":
                    return None
                return float(self.fields[i]["value"])
            i += 1
        return None

    def get_bool(self, value):
        i = 0
        while i < len(self.fields):
            if self.fields[i]["name"] == value:
                if self.fields[i]["value"] == "True":
                    return True
                return False
            i+=1
        return False