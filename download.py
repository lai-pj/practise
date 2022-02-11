import baostock as bs
import pandas as pd
import os
import datetime


output = './predict'
last_day_file = './last_day.txt'
csv_file = './stock_code_2020_12_31.csv'
date_start = '2020-01-01'
date_end = '2034-12-31'
pid_flie = './pid.txt'


def mkdir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_last_day():
    with open(last_day_file,'r') as f:
        return f.readline()

def write_last_day(day):
    with open(last_day_file,'w') as f:
        f.write(day)
        
def start_check():
    with open(pid_flie,'rw') as f:
        run = f.readline()
        if 'Y' == run:
            print('last program is running')
            exit()
        f.write('Y')
    
def end_program():
    with open(pid_flie,'w') as f:
        f.write('N')
    

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
        self.exit()

    def run_sp(self, code):
        #print(f'processing {code} ')
        df_code = bs.query_history_k_data_plus(code, self.fields,
                                               start_date=self.date_start,
                                               end_date=self.date_end).get_data()
        df_code.to_csv(f'{self.output_dir}/{code}.csv', index=False)
        
    def get_code_df(self, code):
        df_code = bs.query_history_k_data_plus(code, self.fields,
                                               start_date=self.date_start,
                                               end_date=self.date_end).get_data()
        return df_code


if __name__ == '__main__':
    start_check()

    #非周六日
    if datetime.datetime.today().weekday() not in (5,6):
        #读取上次下载日期
        last_day = get_last_day()
        today = datetime.date.today()
        today_str = str(today)
        if today_str != last_day:
            print('today is not last_day')
            #下载正式评估数据
            downloader = Downloader(output, date_start=date_start, date_end=date_end)
            data_df = pd.read_csv(csv_file, encoding='ANSI')
            #随机打乱
            data_df.sample(frac=1)
            not_today = 0
            for index, row in data_df.iterrows():
                if index % 100 == 0 and index != 0:
                    print(index)
                row_code = row['code']
                code_df = downloader.get_code_df(row_code)
                code_df.to_csv(f'{output}/{row_code}.csv', index=False)
                #前10条记录判断是否下载了当天数据
                if index < 10 and today_str != code_df.tail(1)['date']:
                    print('code_df last date is not today_str')
                    not_today += 1
                
                if not_today > 5:
                    print('not_today is more than 5')
                    downloader.exit()
                    end_program()
                    exit()
                
            downloader.exit()    
            write_last_day(today_str)
        else:
            print('today is last_day')
    
    end_program()
