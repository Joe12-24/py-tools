import pandas as pd

# 璇诲彇鍘熷 Excel 鏂囦欢璺緞鍜岃緭鍑烘枃浠惰矾寰�
input_excel_file = '鍑屽織鎺ュ彛涓€瑙�.xlsx'  # 鏇挎崲涓轰綘鐨凟xcel鏂囦欢璺緞
output_excel_file = 'output_鍔熻兘鍙穇鍔熻兘鍚嶇О鍐呭11.xlsx'  # 杈撳嚭鏂囦欢璺緞

# 浣跨敤 ExcelFile 鍔犺浇 Excel 鏂囦欢
xls = pd.ExcelFile(input_excel_file)
data_dict = {"鍔熻兘鍙�": [], "鍔熻兘鍚嶇О": []}
# 鍒涘缓涓€涓柊鐨� Excel 鏂囦欢锛屽苟璁剧疆 engine='openpyxl' 浠ユ敮鎸佸啓鍏�
with pd.ExcelWriter(output_excel_file, engine='openpyxl') as writer:
    for sheet_name in xls.sheet_names:
        # 璇诲彇姣忎釜 sheet 鐨勬暟鎹紝鍙彁鍙栫浜屽垪鍜岀涓夊垪
        df = pd.read_excel(xls, sheet_name=sheet_name, usecols=[1, 2])  # 鍙彁鍙栫浜屽垪鍜岀涓夊垪

        # 鍒濆鍖栫┖瀛楀吀鐢ㄤ簬瀛樺偍鎻愬彇鐨勫姛鑳藉彿鍜屽姛鑳藉悕绉扮殑鍐呭
       

        # 寰幆閬嶅巻姣忎竴琛屽苟澶勭悊
        for index, row in df.iterrows():
            # 鍙鐞嗙浜屽垪鍜岀涓夊垪
            second_col_value = row.iloc[0].strip() if isinstance(row.iloc[0], str) else ''
            third_col_value = row.iloc[1].strip() if isinstance(row.iloc[1], str) else ''

            # 鎻愬彇 "鍔熻兘鍙�" 鍚庨潰鐨勫唴瀹�
            if second_col_value == "鍔熻兘鍙�":
                current_func_num = third_col_value
                # print(current_func_num)

                # 鑾峰彇涓嬩竴琛岀殑鍔熻兘鍚嶇О
                if index + 1 < len(df):  # 纭繚涓嬩竴琛屽瓨鍦�
                    next_row = df.iloc[index + 1]
                    current_func_name = next_row.iloc[1].strip() if isinstance(next_row.iloc[1], str) else ''
                else:
                    current_func_name = ''  # 濡傛灉娌℃湁涓嬩竴琛岋紝鍒欏姛鑳藉悕绉颁负绌�

                # 灏嗘彁鍙栫殑鍔熻兘鍙峰拰鍔熻兘鍚嶇О娣诲姞鍒板瓧鍏�
                data_dict["鍔熻兘鍙�"].append(current_func_num)
                data_dict["鍔熻兘鍚嶇О"].append(current_func_name)

        # 鍒涘缓鏂扮殑 DataFrame 淇濆瓨鎻愬彇鍚庣殑鏁版嵁
                result_df = pd.DataFrame(data_dict)
            # print(data_dict)
            # 灏嗙粨鏋滃啓鍏ュ埌鏂扮殑 Excel 鏂囦欢
    result_df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f"鎻愬彇鍚庣殑鏁版嵁宸蹭繚瀛樺埌 {output_excel_file} 涓€�")
