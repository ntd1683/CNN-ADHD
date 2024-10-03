import re
import pandas as pd


def extract_number_or_keep(text):
    # Kiểm tra xem đầu vào có phải là chuỗi không
    if isinstance(text, str):
        # Loại bỏ dấu cách thừa nếu có
        clean_text = text.strip()

        # Kiểm tra nếu chứa phần trăm, ưu tiên lấy số phần trăm
        percent_match = re.search(r'(\d+)%', clean_text)
        if percent_match:
            return int(percent_match.group(1))

        # Nếu không có phần trăm, tìm số thập phân
        number_match = re.search(r'(\d+\.\d+)', clean_text)
        if number_match:
            # Kiểm tra nếu số có phần thập phân
            if '.' in number_match.group(1):
                return float(number_match.group(1))
            else:
                return int(number_match.group(1))

        # Nếu không có số, giữ lại văn bản
        return text
    else:
        # Nếu không phải chuỗi, trả về giá trị nguyên vẹn
        if text < 1:
            return text*100
        return text

def process_data_frequency(data):
    result = []
    for item in data:
        text = extract_number_or_keep(item)
        if isinstance(text, str) and text == item:
            text = f"Văn bản: {text}"
        else:
            if 0 <= text <= 25:
                text = 0
            elif 25 < text <= 50:
                text = 1
            elif 50 < text <= 75:
                text = 2
            else:
                text = 3
        result.append(text)
    return result

file_path = './data.xlsx'
df = pd.read_excel(file_path)

# print("Danh sách các cột trong DataFrame:")
# print(df.columns)

response_mapping = {
    "Không": 0,
    "Không Bao Giờ": 0,
    "Hiếm Khi": 1,
    "Thỉnh Thoảng": 2,
    "Thường Xuyên": 3,
    "Có": 1,
    "Chưa": 0,
    "Rồi": 1,
}

columns_to_convert = [
    'Hiện tại bạn có đang làm dụng thuốc hay chất gì đó không ?',
    'Hiện tại bạn có đang sử dụng thuốc liên quan đến thần kinh hay tâm thần gì không ?',
    'Trong nhà của bạn, có ai bị bệnh liên quan đến tâm thần, hoặc thần kinh không ?',
    'Trong nhà của bạn, có ai dùng chất kích thích không ?',
    'Đôi khi bạn có cảm thấy mình từng bị tự kỷ không ?',
    'Đôi khi bạn có cảm thấy mình từng có các triệu chứng như trầm cảm , tự kỉ hoặc cảm xúc bất thường trong thời gian ngắn không(ví dụ: cảm thấy vui bất thường hoặc dễ bị xúc động chỉ qa một video hoặc overthink có động lực trong thời gian ngắn sau đó lại mất đi dù cố tìm lại nhưng cũng không được như lúc đầu)',
    'Bạn thường xuyên làm mất, thất lạc hoặc làm hỏng những thứ cần thiết để hoàn thành công việc (ví dụ như điện thoại, kính mắt, giấy tờ, ví, chìa khóa, v.v.) như thế nào?',
    'Bạn thường tránh né, không thích hoặc miễn cưỡng tham gia vào các nhiệm vụ đòi hỏi nỗ lực tinh thần hoặc suy nghĩ liên tục như thế nào?',
    'Bạn thường xuyên bồn chồn, gõ tay, gõ chân hoặc ngọ nguậy trên ghế, Rung Chân Không như thế nào?',
    "Bạn có thường xuyên cảm thấy mình 'đang di chuyển', hành động như thể bạn 'được điều khiển bởi một động cơ' không (ví dụ, bạn không thể hoặc cảm thấy không thoải mái khi phải đứng yên trong một khoảng thời gian dài, chẳng hạn như trong nhà hàng hoặc cuộc họp)?",
    'Bạn thường rời khỏi chỗ ngồi bao nhiêu lần trong những tình huống mà người ta yêu cầu bạn phải ngồi yên (ví dụ: rời khỏi chỗ làm việc hoặc văn phòng)?',
    'Bạn có thường xuyên cảm thấy bồn chồn - muốn ra ngoài và làm gì đó không?',
    'Bạn thường buột miệng trả lời trước khi câu hỏi được nói xong bao nhiêu lần (ví dụ, khi hoàn thành câu của người khác hoặc không thể chờ đến lượt mình trong một cuộc trò chuyện)  Hoặc có bao giờ hành động nóng vội dẫn tới tình trạng nghĩ tới đâu làm tới đó không?',
    'Bạn thường xuyên ngắt lời hoặc xen vào chuyện của người khác như xen vào cuộc trò chuyện hoặc chiếm mất việc của người khác như thế nào ?',
    'Bạn thường xuyên khó chịu khi người khác làm một việc gì đó quá lâu, và không hoàn thành trước mặt bạn không ?',
    'Bạn đã bao giờ cảm thấy như vậy hoặc ước rằng mình đã chết chưa?',
    'Bạn có lo lắng về điều gì không hoặc có điều gì khiến bạn thực sự sợ hãi không?',
    'Qua các câu hỏi ở trên bạn nghĩ mình có triệu chứng hoặc bản thân nhận thức được mình có một số triệu chứng đã xuất hiện rồi không?',
    'Các triệu chứng có xuất hiện ở ít nhất hai hoặc nhiều bối cảnh (ví dụ: ở nhà và trường học) không?',
    'Bạn thường hay để quên các vật dụng hay sử dụng hoặc đồ vật vừa mới cầm với tần suất như thế nào ?',
    'Bạn có thường hay có cảm giác động lực ảo làm việc với cường độ cao trong thời gian dài với 1 thứ gì đó trong 1 khoảng thời gian rồi lại bỏ ngang không',
    'Bạn có thường hay làm việc riêng khi đi học đi làm không ?',
    'Bạn đã bao giờ tự áp đặt bản thân phải làm việc quá nhiều dẫn đến mất phương hướng chán nản mất hết động lực chưa?',
]

for col in columns_to_convert:
    if col in df.columns:
        # Chuyển đổi giá trị rỗng, null hoặc chuỗi rỗng thành 0
        df[col] = df[col].replace("", 0)  # Thay thế chuỗi rỗng
        df[col] = df[col].fillna(0)  # Thay thế giá trị null
        df[col] = df[col].map(response_mapping).fillna(0)  # Giữ lại giá trị gốc nếu không ánh xạ được
        df[col] = df[col].infer_objects()  # Xác định kiểu dữ liệu
    else:
        print(f"Cột '{col}' không tồn tại trong DataFrame.")

columns_to_drop = [
    "Dấu thời gian",
    "Bạn tên là gì ?",
    "Bạn bao nhiêu tuổi ?",
    "Hiện tại bạn đang làm gì ? ( sinh viên hay đi làm , làm về nghành gì , sinh viên ngành gì ? )",
    "Những điều gì khiến bạn buồn?",
    "Cảm giác buồn này xuất hiện thường xuyên như thế nào?",
    "Tần suất bạn tập trung làm 1 việc gì đó liên tục với thời gian dài ? Hoặc thời gian mà bạn trong thời gian bạn làm việc gì đó yêu thích tối đa bao lâu ?",
    "Bạn có bao giờ nghi ngờ mình bị ADHD không ? Từ bao giờ ?",
    "Thời Gian Bắt Đầu Đo HRV",
    "Thời Gian Kết Thúc Đo HRV",
    "Điểm Số Đo HRV",
    "Trạng thái đo HRV"
]

df = df.drop(columns=columns_to_drop)

last_col = df.columns[-1]
df[last_col] = df[last_col].replace("", 0)
df[last_col] = df[last_col].fillna(0)
df[last_col] = df[last_col].map(response_mapping).fillna(0)
df[last_col] = df[last_col].infer_objects()

# get frequency of each value in the last column
key = "Trong 1h tiếng hoặc thời gian xem 1 chương trình tần suất bạn thay đổi tư thế hoặc bấm điện thoại ,đọc sách làm việc khác là bao nhiêu lần và nó chiếm bao nhiêu % bộ phim"
print(df[key])
df[key] = process_data_frequency(df[key])
print("svs : ", df["Trong 1h tiếng hoặc thời gian xem 1 chương trình tần suất bạn thay đổi tư thế hoặc bấm điện thoại ,đọc sách làm việc khác là bao nhiêu lần và nó chiếm bao nhiêu % bộ phim"])

print("Dữ liệu sau khi chuyển đổi:")
print(df.head())

output_file = 'processed_data.csv'
df.to_csv(output_file, index=False)

print(f"File đã được xử lý và lưu tại: {output_file}")
