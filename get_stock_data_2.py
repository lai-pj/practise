import baostock as bs
import pandas as pd
import os


OUTPUT = './stockdata'


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


class Downloader(object):
    def __init__(self,
                 output_dir,

                 date_start='1990-01-01',
                 date_end='2020-03-23'):
        self._bs = bs
        bs.login()
        self.date_start = date_start
        # self.date_end = datetime.datetime.now().strftime("%Y-%m-%d")
        self.date_end = date_end
        self.output_dir = output_dir
        self.fields = "date,code,open,high,low,close,volume,amount," \
                      "adjustflag,turn,tradestatus,pctChg,peTTM," \
                      "pbMRQ,psTTM,pcfNcfTTM,isST"

    def exit(self):
        bs.logout()

    def get_codes_by_date(self, date):
        print(date)
        stock_rs = bs.query_all_stock(date)
        stock_df = stock_rs.get_data()
        print(stock_df)
        return stock_df

    def run(self):
        stock_df = self.get_codes_by_date(self.date_end)
        stock_df.to_csv('D:/stock_code.csv', index=False)
        # for index, row in stock_df.iterrows():
        #     print(f'processing {row["code"]} {row["code_name"]}')
            # df_code = bs.query_history_k_data_plus(row["code"], self.fields,
            #                                        start_date=self.date_start,
            #                                        end_date=self.date_end).get_data()
            # df_code.to_csv(f'{self.output_dir}/{row["code"]}.{row["code_name"].replace("*","")}.csv', index=False)
        self.exit()

    def run_sp(self, code):
        print(f'processing {code} ')
        df_code = bs.query_history_k_data_plus(code, self.fields,
                                               start_date=self.date_start,
                                               end_date=self.date_end).get_data()
        df_code.to_csv(f'{self.output_dir}/{code}.csv', index=False)
        # print(df_code)
        # self.exit()


if __name__ == '__main__':
    # # 获取全部股票的日K线数据
    # mkdir('./stockdata/train')
    # downloader = Downloader('./stockdata/train', date_start='1980-01-01', date_end='2019-12-31')
    # downloader.run()
    #下载训练数据
    # downloader = Downloader('D:/stockdata/stock_500', date_start='2010-01-01', date_end='2024-12-31')
    # data_df = pd.read_csv('D:/stock_500.csv')
    # for index, row in data_df.iterrows():
    #     if index % 100 == 0 and index != 0:
    #         print(index)
    #     downloader.run_sp(row['code'])
    #下载正式评估数据
    downloader = Downloader('D:/stockdata/predict', date_start='2020-01-01', date_end='2024-12-31')
    data_df = pd.read_csv('D:/stockdata/stock_code_2020_12_31.csv', encoding='ANSI')
    for index, row in data_df.iterrows():
        if index % 100 == 0 and index != 0:
            print(index)
        downloader.run_sp(row['code'])
