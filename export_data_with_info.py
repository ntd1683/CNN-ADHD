# Đọc dữ liệu
import pandas as pd

file_pathAdhd = './adhd_prediction_results.csv'
dfAdhd = pd.read_csv(file_pathAdhd)

print(dfAdhd.head())

column_mapping_ADHD = {
    'emotions': 'Cảm xúc không ổn định',
    'autism': 'Tự kỷ',
    'stimulant_use': 'Dùng chất kích thích',
    'hereditary_mental_illness': 'Di truyền',
    'Predicted_ADHD': 'Dự đoán ADHD',
    'Actual_ADHD': 'Thực tế ADHD',
    'Prediction_Probability': 'Dự đoán xác suất',
}

dfAdhd.rename(columns=column_mapping_ADHD, inplace=True)
print("\nTên các cột sau khi đổi:")
print(dfAdhd.columns)

file_path_data = './data.xlsx'
df_data = pd.read_excel(file_path_data)

print(df_data.head())

column_mapping = {
    'Địa chỉ email': 'Email',
}

df_data.rename(columns=column_mapping, inplace=True)

# Merge
merged_df = pd.merge(df_data, dfAdhd, on="Email", how="inner")

print(merged_df.head())
print(merged_df.columns)

columns_to_select = [
    "Dấu thời gian", "Email", "Bạn tên là gì ?", "Bạn bao nhiêu tuổi ?",
'Hiện tại bạn đang làm gì ? ( sinh viên hay đi làm , làm về nghành gì , sinh viên ngành gì ? )',
    "Dự đoán ADHD", "Thực tế ADHD", "Dự đoán xác suất",'Cảm xúc không ổn định',
    'Tự kỷ', 'Dùng chất kích thích', 'Di truyền',
    'Qua các câu hỏi ở trên bạn nghĩ mình có triệu chứng hoặc bản thân nhận thức được mình có một số triệu chứng đã xuất hiện rồi không?',
    'Các triệu chứng có xuất hiện ở ít nhất hai hoặc nhiều bối cảnh (ví dụ: ở nhà và trường học) không?',
    # "Bạn đã bao giờ ? Đôi khi nằm im một chỗ không làm gì cả trong nhiều giờ liền ?\r\nNhiều ý tưởng nảy ra trong đầu suy nghĩ táo bạo, não bộ nhạy bén hiểu vấn đề nhanh phân tích tốt ?",
    'Bạn đã bao giờ ? Đôi khi nằm im một chỗ không làm gì cả trong nhiều giờ liền ?\nNhiều ý tưởng nảy ra trong đầu suy nghĩ táo bạo, não bộ nhạy bén hiểu vấn đề nhanh phân tích tốt ?',
    "Bạn có bao giờ nghi ngờ mình bị ADHD không ? Từ bao giờ ?",
    "Thời Gian Bắt Đầu Đo HRV",
    "Thời Gian Kết Thúc Đo HRV",
    "Điểm Số Đo HRV",
    "Trạng thái đo HRV",
]

final_df = merged_df[columns_to_select]

print(final_df.head())
final_df.to_csv('final_merged_data.csv', index=False)