import pandas as pd
import networkx as nx
import argparse

def tim_vector(tenda,pretenda): # Tim cac vector tren giang do
    Start_point = [i for i in tenda if pretenda[tenda.index(i)] == '-'] #Tìm start point
    #print(Start_point)

    # Liệt kê các vector:
    ##Thêm vector start point
    vector = [["Start",i] for i in Start_point] 
    #print(vector)

    ##Thêm vector trung gian
    for i in range(len(pretenda)): 
        if pretenda[i] != "-" and len(pretenda[i]) == 1:
            vector.append([pretenda[i],tenda[i]])
        elif len(pretenda[i]) > 1:
            Stats = pretenda[i].split(",")
            for k in range(len(Stats)):
                vector.append([Stats[k],tenda[i]]) 
    #print(vector)

    ##Tìm end point
    End_point = []
    for i in range(len(tenda)):
        a = 0
        for k in range(len(pretenda)):
            if tenda[i] in pretenda[k]:
                a += 1
        if a == 0:
            End_point.append(tenda[i])
    #print(End_point)

    vector.extend([[i,'End'] for i in End_point])
    #print(vector)
    return vector

def all_paths(G): # Xuat ra cac con duong
    roots = (v for v, d in G.in_degree() if d == 0)
    leaves = [v for v, d in G.out_degree() if d == 0]
    all_paths = []
    for root in roots:
        paths = nx.all_simple_paths(G, root, leaves)
        all_paths.extend(paths)
    return all_paths

def pathsf(tenda,pretenda): # Xac dinh cac con duong
    # Xac dinh cac con duong
    ## Xac dinh cac vecto
    vector = tim_vector(tenda,pretenda)
    #print(vector)
    ## Xac dinh cac con duong
    G = nx.DiGraph()
    G.add_edges_from(vector)
    paths = all_paths(G)
    #print(lisotoString(paths))
    return paths

def Tim_gantt(paths,tenda,tg1): # Rà thời gian thực hiện dự án của các con đường 
    g_list = []
    for i in range(len(paths)):
        g_val = []
        for k in range(1,len(paths[i])-1):
            for j in range(len(tenda)):
                if tenda[j] == paths[i][k]:
                    g_val.append(tg1[j])
        g_list.append(g_val)
    return g_list

class Ganttc(): 
    def __init__(self,tenda,paths,tg1):
        self.tenda = tenda
        self.paths = paths
        self.tg1 = tg1
        self.g_list = Tim_gantt(self.paths,self.tenda,self.tg1)
    #print(g_list)

    def time(self): # Tra ve thoi gian hoan thanh du an    
        return [sum(i) for i in self.g_list]
        #print("Thời gian hoàn thành: "+ str(g_val_list))

    def gantt(self): # Tra ve duong gantt
        max_tg = max(self.time())
        #print(max_tg)

        Gantt = [self.time().index(max_tg)]
        return Gantt

# Tạo hàm tính EST và EFT
def Find_pp(paths,nameac): # Tim cac diem lien ke truoc cua 1 diem tron cac con duong
    beforeac = [sublist[i-1] for sublist in paths for i in range(len(sublist)) if sublist[i] == nameac] # Lay cac ac nam truoc nameac trong cac con duong
    #print(beforeac)
    beforeac_uniq = []
    tem = [beforeac_uniq.append(i) for i in beforeac if i not in beforeac_uniq] # Chon loc duy nhat
    #print(beforeac_uniq)
    return beforeac_uniq
#print(Find_pp(paths,nameac))

def Find_est(tenac,te_vals,paths): # Tìm est vaf eft cua cac cong viec
    est_lib = {tenac[i]:[0,te_vals[i]] for i in range(len(tenac))} # Tao thu vien est
    #print(est_lib)

    for path in paths:
        for i in range(2,len(path)-1): # Tinh cac 1 input truoc
            pp = Find_pp(paths,path[i])
            #print(pp)
            if len(pp) == 1:
                est_lib[path[i]][0] = est_lib[pp[0]][0]+est_lib[pp[0]][1]
        
        for i in range(2,len(path)-1): # Tinh cac hai input tro len
            pp = Find_pp(paths,path[i])
            #print(pp)
            if len(pp) > 1:
                est_lib[path[i]][0] = max([est_lib[k][0]+est_lib[k][1] for k in pp])
        
        for i in range(2,len(path)-1): # Tinh lai cac 1 input
            pp = Find_pp(paths,path[i])
            #print(pp)
            if len(pp) == 1:
                est_lib[path[i]][0] = est_lib[pp[0]][0]+est_lib[pp[0]][1]

    #print(est_lib)
    est_vals = [est_lib[i][0] for i in est_lib]
    eft_vals = [sum(est_lib[i]) for i in est_lib]
    #print(est_vals)
    return est_vals, eft_vals

est_find = lambda ac, pre_ac ,du: Find_est(ac,du,pathsf(ac,pre_ac)) 

def FindPara(data1,time_dg):
    ## Khai báo dữ liệu
    ac = list(data1.iloc[:,0]) # ten cac du an
    #print(ac)
    pre_ac = list(data1.iloc[:,1]) # cac du an lien truoc
    #print(pre_ac)
    du = list(data1.iloc[:,2]) # duration

    ## Tim EST (thoi gian bat dau som) va EFT (thoi gian ket thuc som) cua cac cong tac
    est, eft = est_find(ac, pre_ac ,du)
    #print(est)
    #print(eft)

    ## Xem cac du an co thoi gian bat dau be hon hoac bang thoi gian danh gia
    index_dg = [i for i in range(len(eft)) if est[i] < time_dg] # index cua cac du an can danh gia
    #print(index_dg)

    est_dg = [est[i] for i in index_dg] # est cua cac du an danh gia
    eft_dg = [eft[i] for i in index_dg] # eft cua cac du an danh gia

    ## Khai bao du lieu danh gia
    ac_dg = [ac[i] for i in index_dg] # Ten cac du an danh gia
    #print(ac_dg)
    du_dg = [du[i] for i in index_dg] # Thoi gian thu hien cua cac du an danh gia
    #print(du_dg)
    cp_dt = [list(data1.iloc[:,3])[i] for i in index_dg] # Chi phi du tinh
    #print(cp_dt)
    cp_tt = [list(data1.iloc[:,4])[i] for i in index_dg] # Chi phi thuc te
    #print(cp_tt)
    com = [i/100 for i in list(data1.iloc[:,5])] # % cong viec hoan thanh
    #print(com)

    ## Tìm thời gian đánh giá dự án
    tg_dg = []
    for i in range(len(ac_dg)):
        if eft_dg[i] > time_dg:
            tg_dg.append(time_dg-est_dg[i])
        else:
            tg_dg.append(du_dg[i])
    #print(tg_dg)

    table = TinhPar(ac_dg,du_dg,cp_dt,cp_tt,com,tg_dg)
    #print(table)

    return table 

def dgtd(sv): #Đánh giá tiến độ thực hiện dự án
    if sv > 0 :
        return "Trước"
    elif sv == 0:
        return "Đúng"
    else:
        return "Trễ"

def dgcp(cv): #Đánh giá chi phi thực hiện dự án
    if cv > 0 :
        return "Dưới"
    elif cv == 0:
        return "Đúng"
    else:
        return "Vượt"

def TinhPar(ct,time,cp_pre,cp_real,per_wor,tdg): #Tinh cac parameter 
    cp_dv = [cp_pre[i]/time[i] for i in range(len(time))] # Chi phi thu te moi tuan (cp_pre/time)
    #print(cp_dv)

    # Tinh PV
    pv = [tdg[i] * cp_dv[i] for i in range(len(tdg))] # Chi phi chi theo ke hoach (chi phí/tuần * thời gian đánh giá)
    #print(pv)

    # Tính EV
    ev = [cp_pre[i]*per_wor[i] for i in range(len(cp_pre))] # Chi phi hoan thanh cong viec theo % công việc thực hiện
    #print(ev)

    ## Tính AC
    ac = cp_real # chi phí thực tế
    #print(ac)

    ## Tính SV 
    sv = [ev[i]-pv[i] for i in range(len(ev))]
    #print(sv)

    ## Tính CV
    cv = [ev[i]-ac[i] for i in range(len(ev))]
    #print(cv)

    ## Tính SPI
    spi = [ev[i]/pv[i] for i in range(len(ev))]
    #print(spi)

    ## Tính CPI
    cpi = [ev[i]/ac[i] for i in range(len(ev))]
    #print(cpi)

    ## Xuât bang
    table = pd.DataFrame(zip(ct,ev,pv,ac,sv,cv,spi,cpi),columns=["CT","EV","PV","AC","SV","CV","SPI","CPI"])
    #print(table)
    return table

def ComAc(table2): # Danh gia chi phi va tien do cac hoat dong trong du an
    ## Đánh giá chi phí và tiến độ cua cac du an
    dgt = list(map(dgtd,list(table2["SV"]))) # Danh gia tien do
    #print(dgt)

    dgc = list(map(dgcp,list(table2["CV"]))) # Danh gia chi phi
    #print(dgc)

    table1 = pd.DataFrame(zip(list(table2["CT"]),dgt,dgc), columns=["CT", "Process", "Cost"])
    #print(table1)
    return table1

def ProPar(table2): #Thong so toan bo du an
     # Tinh cac thong so cho toan bo du an
    ev_pro = sum(table2["EV"])
    pv_pro = sum(table2["PV"])
    ac_pro = sum(table2["AC"])
    sv_pro = ev_pro-pv_pro
    cv_pro = ev_pro-ac_pro
    spi_pro = ev_pro/pv_pro
    cpi_pro = ev_pro/ac_pro

    rs = {"EV":ev_pro,"PV":pv_pro,"AC":ac_pro,"SV":sv_pro,"CV":cv_pro,"SPI":spi_pro,"CPI":cpi_pro}
    return rs

def ComAcPro(propar): # Danh gia du an
     return [dgtd(propar["SV"]),dgcp(propar["CV"])]

def FindParaPro(data3,propar):
    bac = sum(list(data3.iloc[:,3]))
    etc = round((bac-propar["EV"])/propar["CPI"],2)
    eac = propar["AC"]+ etc
    vac = round(bac - eac,2)

    rs = {"BAC":bac,"ETC":etc,"EAC":eac,"VAC":vac}
    #print(rs)
    return rs

def ComplePro(data3,daycheck): # Hoan thien du lieu
    table2 = FindPara(data3,daycheck) # Xuat bang cac chi so cong viec
    #print(table2)

    # Danh gia tien do va chi phi cua cac hoat dong trong du an
    comment = ComAc(table2)
    #print(comment)

    #Thong so toan bo du an
    propar = ProPar(table2)
    #print(propar)

    # Danh gia toan bo du an
    compro = ComAcPro(propar)
    #print(compro)

    parpro = FindParaPro(data3,propar) # Tim cac thong so cua ca du an
    print(parpro)

    ## Tao list tong du an
    tong = ["Tổng DA"]
    tem = [tong.append(propar[i]) for i in propar]
    #print(tong)

    ## Them tong DA vao bang
    table2.loc[len(table2.index)] = tong
    #print(table2)

    ## them danh gia toan bo du an
    comment.loc[len(comment)] = ["Tổng DA"]+compro
    #print(comment.iloc[:,1:])

    table2 = pd.concat([table2,comment.iloc[:,1:]], axis =1, join="inner")
    print(table2)


# Initialize parser
parser = argparse.ArgumentParser()

parser.add_argument("-f", "--input_file")
parser.add_argument("-c", "--check_day")
parser.add_argument("-v",'--version', action='version', version='%(prog)s 1.0',help = 'show version')

# Read arguments from command line
args = parser.parse_args()


data3 = pd.read_csv(args.input_file,sep = "\t") #Doc du lieu
#print(data3)

ComplePro(data3,int(args.check_day))