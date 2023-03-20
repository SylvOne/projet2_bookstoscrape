import pandas as pd

class LoadDatas:
    def __init__(self, datas_to_load):
        self.datas_to_load = datas_to_load

    def to_csv(self):
        df = pd.DataFrame(self.datas_to_load)
        df.to_csv('./csv/book_info_'+self.datas_to_load['category'][0]+'.csv', index=False)