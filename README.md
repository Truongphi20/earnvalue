# Tìm các thông số của phương pháp Giá trị làm ra 
(Chương 5 QLDA)

Dựa vào file input và thời gian đánh giá, tính các thông số.

## Các thông số tính

### Thông số của từng dự án

1. EV (Earned value): Chi phí hoàn thành công việc tương ứng % công việc đã hoàn thành (chi phí dự tính * % hoàn thành cv)
2. PV (Planned time-phased baseline on value): Số tiền phải chi tính đến thời điểm đánh giá (chi phí/tuần * thời gian đánh giá)
3. AC (Actual cost): chi phí thực tế
4. SV (Schedule variance): Độ sai lệch của chi phí theo tiến độ dự án (EV - PV)
5. CV (Cost variance): Độ sai lệch chi phí dự án (EV - AC)
6. SPI (Scheduling performance index): Tỉ lệ chi phí hoàn thành công việc và chi phí theo thời gian (EV/PV) 
7. CPI (Cost performance index): Tỉ lệ chi phí hoàn thành công việc và chi phí thực tế (EV/AC)

### Thông số của cả dự án

Tính các giá trị cho tổng thể dự án:

 - ETC (Estimated cost to complete remaining work): ETC = (BAC − EV)/CPI (page 479)
 - BAC (Total budget of the baseline): Tổng ngân sách trên baseline dự án (page 479)
 - EAC (Expected costs at completion): Dự đoán tổng chi phí khi hoàn thành (EAC = AC + ETC, page 479)
 - VAC (Cost variance at completion): Khoảng tiền còn dư sau dự án (BAC − EAC, page 468)

## Cách sử dụng

### Kiểm tra cài đặt

      python .\Ear_val.py -h
      usage: Ear_val.py [-h] [-f INPUT_FILE] [-c CHECK_DAY] [-v]

    optional arguments:
      -h, --help            show this help message and exit
      -f INPUT_FILE, --input_file INPUT_FILE
      -c CHECK_DAY, --check_day CHECK_DAY
      -v, --version         show version

### Chạy phần mềm
      
       python .\Ear_val.py -f input_file -c check_day
       
Chú giải `input_file`:

- Là file csv, phân các các thành phần bằng tab (tham khảo bt5.3.csv)
- Có thể thay đổi tên header nhưng phải giữ nguyên thứ tự
- Cột 1: Tên công việc
- Cột 2: Tên công việc liền trước
- Cột 3: Thời gian diễn ra công việc
- Cột 4: Tổng chi phí dự định chi cho công việc đó
- Cột 5: Tổng chi phí thực tế phải chi
- Cột 6: Tiến độ hoàn thành công viêc (1 - 100)

`check_day` là ngày thực hiện đánh giá dự án.

### Chạy thử ví dụ

Tìm các chỉ số của các công việc trong dự án như trong file `bt5.3.csv`, tính các chỉ số của các công việc và dự án:

Input:

    .\Ear_val.py -f .\bt5.3.csv -c 15

Output:

    {'BAC': 152000, 'ETC': 67752.13, 'EAC': 147752.13, 'VAC': 4247.87}
            CT       EV       PV     AC       SV      CV       SPI       CPI Process  Cost
    0        A   3000.0   3000.0   3000      0.0     0.0  1.000000  1.000000    Đúng  Đúng
    1        B  25000.0  25000.0  30000      0.0 -5000.0  1.000000  0.833333    Đúng  Vượt
    2        C  12000.0  12000.0  10000      0.0  2000.0  1.000000  1.200000    Đúng  Dưới
    3        D   6000.0  10000.0   7000  -4000.0 -1000.0  0.600000  0.857143     Trễ  Vượt
    4        E   7500.0  16000.0  10000  -8500.0 -2500.0  0.468750  0.750000     Trễ  Vượt
    5        F  28800.0  32000.0  20000  -3200.0  8800.0  0.900000  1.440000     Trễ  Dưới
    6  Tổng DA  82300.0  98000.0  80000 -15700.0  2300.0  0.839796  1.028750     Trễ  Dưới
    

    
    
  
