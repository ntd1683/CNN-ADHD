import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import Conv1D, MaxPooling1D, Flatten, Dense
from keras.optimizers import Adam

# Đọc dữ liệu
data = pd.read_csv('./processed_data.csv', encoding='utf-8')

# In ra tên các cột để kiểm tra
print("Tên các cột gốc:")
print(data.columns)

# Mapping tên cột dài sang tên ngắn
column_mapping = {
    "Địa chỉ email" : "Email",
    "Hiện tại bạn có đang làm dụng thuốc hay chất gì đó không ?": "col1",
    "Hiện tại bạn có đang sử dụng thuốc liên quan đến thần kinh hay tâm thần gì không ?": "col2",
    "Trong nhà của bạn, có ai bị bệnh liên quan đến tâm thần, hoặc thần kinh không ?" : "col3",
    "Trong nhà của bạn, có ai dùng chất kích thích không ?" : "col4",
    "Đôi khi bạn có cảm thấy mình từng bị tự kỷ không ?" : "col5",
    "Đôi khi bạn có cảm thấy mình từng có các triệu chứng như trầm cảm , tự kỉ hoặc cảm xúc bất thường trong thời gian ngắn không(ví dụ: cảm thấy vui bất thường hoặc dễ bị xúc động chỉ qa một video hoặc overthink có động lực trong thời gian ngắn sau đó lại mất đi dù cố tìm lại nhưng cũng không được như lúc đầu)" : "col6",
    "Bạn thường xuyên làm mất, thất lạc hoặc làm hỏng những thứ cần thiết để hoàn thành công việc (ví dụ như điện thoại, kính mắt, giấy tờ, ví, chìa khóa, v.v.) như thế nào?": "col7",
    "Bạn thường tránh né, không thích hoặc miễn cưỡng tham gia vào các nhiệm vụ đòi hỏi nỗ lực tinh thần hoặc suy nghĩ liên tục như thế nào?": "col8",
    "Bạn thường xuyên bồn chồn, gõ tay, gõ chân hoặc ngọ nguậy trên ghế, Rung Chân Không như thế nào?": "col9",
    "Bạn có thường xuyên cảm thấy mình 'đang di chuyển', hành động như thể bạn 'được điều khiển bởi một động cơ' không (ví dụ, bạn không thể hoặc cảm thấy không thoải mái khi phải đứng yên trong một khoảng thời gian dài, chẳng hạn như trong nhà hàng hoặc cuộc họp)?": 'col10',
    "Bạn thường rời khỏi chỗ ngồi bao nhiêu lần trong những tình huống mà người ta yêu cầu bạn phải ngồi yên (ví dụ: rời khỏi chỗ làm việc hoặc văn phòng)?": "col11",
    "Bạn có thường xuyên cảm thấy bồn chồn - muốn ra ngoài và làm gì đó không?": "col12",
    "Bạn thường buột miệng trả lời trước khi câu hỏi được nói xong bao nhiêu lần (ví dụ, khi hoàn thành câu của người khác hoặc không thể chờ đến lượt mình trong một cuộc trò chuyện)  Hoặc có bao giờ hành động nóng vội dẫn tới tình trạng nghĩ tới đâu làm tới đó không?": "col13",
    "Bạn thường xuyên ngắt lời hoặc xen vào chuyện của người khác như xen vào cuộc trò chuyện hoặc chiếm mất việc của người khác như thế nào ?": "col14",
    "Bạn thường xuyên khó chịu khi người khác làm một việc gì đó quá lâu, và không hoàn thành trước mặt bạn không ?": "col15",
    "Bạn đã bao giờ cảm thấy như vậy hoặc ước rằng mình đã chết chưa?": "col16",
    "Bạn có lo lắng về điều gì không hoặc có điều gì khiến bạn thực sự sợ hãi không?": "col17",
    "Qua các câu hỏi ở trên bạn nghĩ mình có triệu chứng hoặc bản thân nhận thức được mình có một số triệu chứng đã xuất hiện rồi không?": "col18",
    "Các triệu chứng có xuất hiện ở ít nhất hai hoặc nhiều bối cảnh (ví dụ: ở nhà và trường học) không?": "col19",
    "Bạn thường hay để quên các vật dụng hay sử dụng hoặc đồ vật vừa mới cầm với tần suất như thế nào ?": "col20",
    "Bạn có thường hay có cảm giác động lực ảo làm việc với cường độ cao trong thời gian dài với 1 thứ gì đó trong 1 khoảng thời gian rồi lại bỏ ngang không": "col21",
    "Trong 1h tiếng hoặc thời gian xem 1 chương trình tần suất bạn thay đổi tư thế hoặc bấm điện thoại ,đọc sách làm việc khác là bao nhiêu lần và nó chiếm bao nhiêu % bộ phim": "col22",
    "Bạn có thường hay làm việc riêng khi đi học đi làm không ?": "col23",
    "Bạn đã bao giờ tự áp đặt bản thân phải làm việc quá nhiều dẫn đến mất phương hướng chán nản mất hết động lực chưa?": "col24",
    "Bạn đã bao giờ ? Đôi khi nằm im một chỗ không làm gì cả trong nhiều giờ liền ?\r\nNhiều ý tưởng nảy ra trong đầu suy nghĩ táo bạo, não bộ nhạy bén hiểu vấn đề nhanh phân tích tốt ?" : "col25",
}

# Đổi tên cột
data.rename(columns=column_mapping, inplace=True)

# In ra tên các cột sau khi đổi tên
print("\nTên các cột sau khi đổi:")
print(data.columns)

# Chuẩn bị dữ liệu
features = ['impulsive_behaviors', 'restlessness', 'procrastination', 'losing_items', 'unable_to_sit_still']

feature_columns = {
    'impulsive_behaviors': ['col13', 'col14', 'col15'],
    'restlessness': ['col9', 'col10', 'col11', 'col12', 'col23'],
    'procrastination': ['col8', 'col21', 'col24'],
    'losing_items': ['col7', 'col20'],
    'unable_to_sit_still': ['col11', 'col22']
}
#
# Tạo hàm để tính điểm cho mỗi đặc trưng
def calculate_score(row, feature):
    return sum(row[col] for col in feature_columns[feature])

# Tính điểm cho mỗi đặc trưng
X = data.apply(lambda row: pd.Series({feature: calculate_score(row, feature) for feature in features}), axis=1)

# Tính nhãn ADHD (3/5 true theo quy tắc)
y = (X >= np.array([6, 9, 5, 4, 4])).sum(axis=1) >= 3

# Chuẩn hóa dữ liệu
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Reshape dữ liệu cho CNN (samples, time steps, features)
X_reshaped = X_scaled.reshape((X_scaled.shape[0], X_scaled.shape[1], 1))

# Chia dữ liệu
X_train, X_test, y_train, y_test = train_test_split(X_reshaped, y, test_size=0.2, random_state=42)

# Xây dựng mô hình CNN
model = Sequential([
    Conv1D(filters=64, kernel_size=2, activation='relu', input_shape=(5, 1)),
    MaxPooling1D(pool_size=2),
    Flatten(),
    Dense(50, activation='relu'),
    Dense(1, activation='sigmoid')
])

# Biên dịch mô hình
model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

# Huấn luyện mô hình
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# Đánh giá mô hình
loss, accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f'Test accuracy: {accuracy:.4f}')

# Dự đoán cho toàn bộ dữ liệu
all_predictions = model.predict(X_reshaped)
predictions_binary = (all_predictions > 0.5).astype(int).flatten()

# Tạo DataFrame kết quả
results_df = pd.DataFrame({
    'Email': data['Email'] if 'Email' in data.columns else range(len(data)),  # Sử dụng số thứ tự nếu không có cột Email
    'Predicted_ADHD': predictions_binary,
    'Actual_ADHD': y,
    'Prediction_Probability': all_predictions.flatten()
})

# Thêm các cột đặc trưng
for feature in features:
    results_df[feature] = X[feature]

# Lưu kết quả vào file CSV
results_df.to_csv('adhd_prediction_results.csv', index=False)

print("Kết quả đã được lưu vào file 'adhd_prediction_results.csv'")

# In một số thống kê
print("\nThống kê:")
print(f"Tổng số mẫu: {len(results_df)}")
print(f"Số mẫu được dự đoán là ADHD: {results_df['Predicted_ADHD'].sum()}")
print(f"Số mẫu thực tế là ADHD: {results_df['Actual_ADHD'].sum()}")
