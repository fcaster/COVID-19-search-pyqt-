import sys
import mainwindow
import requests
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets

class mainwindow(QMainWindow):
    '''
    主窗口类
    '''
    def __init__(self):
        super().__init__()
        # 属性定义
        '''
        self.provinceName:  province name of China.
                            type: list
        self.url:   ulr list
                    type: list
        self.data:  infomation list
                    type: list
        self.ui:    Ui_mainwindow类实例
                    type: Ui_mainwindow
        '''
        self.provinceName = ['上海市','云南省', '内蒙古自治区',  '北京市',  '台湾', '吉林省', '四川省', '天津市', \
                    '宁夏回族自治区', '安徽省', '山东省', '山西省', '广东省', '广西壮族自治区','新疆维吾尔自治区',\
                    '江苏省', '江西省', '河北省', '河南省','浙江省', '海南省', '湖北省', '湖南省', '澳门',\
                    '甘肃省', '福建省', '西藏自治区', '贵州省', '辽宁省', '重庆市', '陕西省', '青海省', '香港', '黑龙江省']
        self.url = \
            [
                # 0 按省份名称获取信息的接口
                'https://lab.isaaclin.cn/nCoV/api/area?latest=1&province=', \
                # 1 获取所有地区信息
                'https://lab.isaaclin.cn/nCoV/api/area',\
                # 2 获取信息
                'https://lab.isaaclin.cn/nCoV/api/news?',\
                # 3 谣言信息
                'https://lab.isaaclin.cn/nCoV/api/rumors?'
            ]
            
        self.data = []

        # 初始化类
        self.ui = test3.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton_2.setToolTip("1. 本项目完全出于公益目的，API无偿开放给非商业目的人士使用，\n\
如果未来用作商业目的或产生任何不必要的版权纠纷，本项目不负任何责任；\n\
2. 本项目仅获取丁香园的疫情数据并将其储存为时间序列，数据所有权为丁香园,\n\
本人无法授权任何个人或团体在科研或商业项目中使用本数据，\n\
如有需要,希望您能够联系丁香园并取得许可；")

        reqArea = requests.get(self.url[1])  
        reqNews = requests.get(self.url[2])
        reqRumors = requests.get(self.url[3])
        self.data = reqArea.json()['results']
        self.news = reqNews.json()['results']
        self.rumors = reqRumors.json()['results']
        self.setTree()
        self.refresh()

    def setTree(self):
        '''
        func: 初始化treewidget和treewidget_2
        '''
        self.ui.treeWidget.setColumnCount(5)
        self.ui.treeWidget_2.setColumnCount(5)
        self.ui.treeWidget.setHeaderLabels(["地区", "累计确诊人数","现存确诊人数", "治愈人数", "死亡人数"])
        self.ui.treeWidget_2.setHeaderLabels(["地区", "累计确诊人数","现存确诊人数", "治愈人数", "死亡人数"])
        self.provinceInfo = [QtWidgets.QTreeWidgetItem(self.ui.treeWidget) for i in range(len(self.provinceName))]
        self.countryInfo = [QtWidgets.QTreeWidgetItem(self.ui.treeWidget_2) for i in range(len(self.data)-len(self.provinceName))]

    def refresh(self):
        '''
        function: 获取信息并刷新页面
        '''
        try:
            reqArea = requests.get(self.url[1])
            reqNews = requests.get(self.url[2])
            reqArea.raise_for_status()
        except:
            self.ui.textBrowser.setText("刷新失败")
            return None
        
        self.data = reqArea.json()['results']
        n = 0
        for i in range(len(self.data)):
            if self.data[i]['countryEnglishName'] == "China":
                self.provinceInfo[n].setText(0, str(self.data[i]['provinceName']))
                self.provinceInfo[n].setText(1, str(self.data[i]['confirmedCount']))
                self.provinceInfo[n].setText(2, str(self.data[i]['currentConfirmedCount']))
                self.provinceInfo[n].setText(3, str(self.data[i]['curedCount']))
                self.provinceInfo[n].setText(4, str(self.data[i]['deadCount']))
                if len(self.data[i]['cities']) > 0:

                    cityInfo = [QtWidgets.QTreeWidgetItem(self.provinceInfo[n]) for k in range(len(self.data[i]['cities']))]
                    for j in range(len(self.data[i]['cities'])):
                        cityInfo[j].setText(0, str(self.data[i]['cities'][j]['cityName']))
                        cityInfo[j].setText(1, str(self.data[i]['cities'][j]['confirmedCount']))
                        cityInfo[j].setText(2, str(self.data[i]['cities'][j]['currentConfirmedCount']))
                        cityInfo[j].setText(3, str(self.data[i]['cities'][j]['curedCount']))
                        cityInfo[j].setText(4, str(self.data[i]['cities'][j]['deadCount']))
                n+=1
        n = 0
        for i in range(len(self.data)):
            if self.data[i]['countryEnglishName'] != "China":
                self.countryInfo[n].setText(0, str(self.data[i]['countryName']))
                self.countryInfo[n].setText(1, str(self.data[i]['confirmedCount']))
                self.countryInfo[n].setText(2, str(self.data[i]['currentConfirmedCount']))
                self.countryInfo[n].setText(3, str(self.data[i]['curedCount']))
                self.countryInfo[n].setText(4, str(self.data[i]['deadCount']))
                n+=1

        info = ''
        for i in range(len(self.news)):
            info += ('【' + self.news[i]['title'] + '】\n')
            info += ('    '+self.news[i]['summary'] + '\n')
            info += ("\n消息来源:"+ self.news[i]['sourceUrl'] + '\n')
            info += ("=====================================\n")
        self.ui.textBrowser.setText(info)

        info = ''
        for i in range(len(self.rumors)):
            info += ("虚假信息：" + self.rumors[i]['title']+'\n\n')
            info += ('概述：' + self.rumors[i]['mainSummary']+'\n')
            info += ('内容：' + self.rumors[i]['body']+'\n')
            info += ("=====================================\n")
        self.ui.textBrowser_2.setText(info)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    w = mainwindow()
    w.show()
    sys.exit(app.exec_())
