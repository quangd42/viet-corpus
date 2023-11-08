import sys
import datetime

# Convert Vietnamese text to Telex
TELEX_MAPPING = {
    'áu': 'aus', 'àu': 'auf', 'ảu': 'aur', 'ãu': 'aux', 'ạu': 'auj',
    'ái': 'ais', 'ài': 'aif', 'ải': 'air', 'ãi': 'aix', 'ại': 'aij',
    'áo': 'aos', 'ào': 'aof', 'ảo': 'aor', 'ão': 'aox', 'ạo': 'aoj',
    'áy': 'ays', 'ày': 'ayf', 'ảy': 'ayr', 'ãy': 'ayx', 'ạy': 'ayj',
    'ắu': 'awus', 'ằu': 'awuf', 'ẳu': 'awur', 'ẵu': 'awux', 'ặu': 'auj',
    'ắy': 'awys', 'ằy': 'awyf', 'ẳy': 'awyr', 'ẵy': 'awyx', 'ặy': 'ayj',
    'ấu': 'auas', 'ầu': 'auaf', 'ẩu': 'auar', 'ẫu': 'auax', 'ậu': 'auaj',
    'ấy': 'ayas', 'ầy': 'ayaf', 'ẩy': 'ayar', 'ẫy': 'ayax', 'ậy': 'ayaj',
    'éu': 'eus', 'èu': 'euf', 'ẻu': 'eur', 'ẽu': 'eux', 'ẹu': 'euj',
    'éo': 'eos', 'èo': 'eof', 'ẻo': 'eor', 'ẽo': 'eox', 'ẹo': 'eoj',
    'ếu': 'eues', 'ều': 'euef', 'ểu': 'euer', 'ễu': 'euex', 'ệu': 'euej',
    'ía': 'ias', 'ìa': 'iaf', 'ỉa': 'iar', 'ĩa': 'iax', 'ịa': 'iaj',
    'íu': 'ius', 'ìu': 'iuf', 'ỉu': 'iur', 'ĩu': 'iux', 'ịu': 'iuj',
    'óa': 'oas', 'òa': 'oaf', 'ỏa': 'oar', 'õa': 'oax', 'ọa': 'oaj',
    'ói': 'ois', 'òi': 'oif', 'ỏi': 'oir', 'õi': 'oix', 'ọi': 'oij',
    'ối': 'osoi', 'ồi': 'ofoi', 'ổi': 'oroi', 'ỗi': 'oxoi', 'ội': 'ojoi',
    'ới': 'owis', 'ời': 'owif', 'ởi': 'owir', 'ỡi': 'owix', 'ợi': 'owij',
    'úa': 'uas', 'ùa': 'uaf', 'ủa': 'uar', 'ũa': 'uax', 'ụa': 'uaj',
    'úi': 'uis', 'ùi': 'uif', 'ủi': 'uir', 'ũi': 'uix', 'ụi': 'uij',
    'úy': 'uys', 'ùy': 'uyf', 'ủy': 'uyr', 'ũy': 'uyx', 'ụy': 'uyj',
    'ứa': 'uaws', 'ừa': 'uawf', 'ửa': 'uawr', 'ữa': 'uawx', 'ựa': 'uwj',
    'ứi': 'uiws', 'ừi': 'uiwf', 'ửi': 'uiwr', 'ữi': 'uiwx', 'ựi': 'uiwj',
    'ươ': 'uow', 'ướ': 'uows', 'ườ': 'uowf' ,'ưở': 'uowr', 'ưỡ': 'uowx', 'ượ': 'uowj', #this can be alt
    # Single character
    'ă': 'aw', 'â': 'aa', 'ê': 'ee', 'ô': 'oo', 'ơ': 'ow', 'ư': 'w', 'đ': 'dd',
    'á': 'as', 'à': 'af', 'ả': 'ar', 'ã': 'ax', 'ạ': 'aj', 
    'ắ': 'aws', 'ằ': 'awf', 'ẳ': 'awr', 'ẵ': 'awx', 'ặ': 'awj', 
    'ấ': 'asa', 'ầ': 'afa', 'ẩ': 'ara', 'ẫ': 'axa', 'ậ': 'aja',
    'é': 'es', 'è': 'ef', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej', 
    'ế': 'ese', 'ề': 'efe', 'ể': 'ere', 'ễ': 'exe', 'ệ': 'eje',
    'í': 'is', 'ì': 'if', 'ỉ': 'ir', 'ĩ': 'ix', 'ị': 'ij',
    'ó': 'os', 'ò': 'of', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj', 
    'ố': 'oso', 'ồ': 'ofo', 'ổ': 'oro', 'ỗ': 'oxo', 'ộ': 'ojo',
    'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
    'ú': 'us', 'ù': 'uf', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj', 
    'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
    'ý': 'ys', 'ỳ': 'yf', 'ỷ': 'yr', 'ỹ': 'yx', 'ỵ': 'yj',
    }

# Maximum number of output file
OUTPUT_COUNT_LIMIT = 20
OUTPUT_PATH = "data/output/"


def convert_word_to_telex(word: str, telex_mapping: dict) -> str:
    telex_word = ''
    i = 0
    word_len = len(word)

    while i < word_len:
        found = False

        # Try to find multi-character combinations in decreasing order of length
        for j in range(min(5, word_len - i), 0, -1):
            subword = word[i:i+j]
            if subword in telex_mapping:
                telex_word += telex_mapping[subword]
                i += j
                found = True
                break

        if not found:
            telex_word += word[i]
            i += 1

    return telex_word


def convert_line_to_telex(line: str, telex_mapping: dict) -> str:
    telex_line = [convert_word_to_telex(word.lower(), telex_mapping) for word in line.split()]
    return " ".join(telex_line)


def convert_multiple_lines_to_telex(input_file: str, telex_mapping: dict, number_of_lines: int) -> int:
    try:
        with open(input_file, encoding="utf-8") as f:
            output_count = 1
            
            temp_line_count = number_of_lines
            telex_lines = []
            
            for line in f:
                if temp_line_count > 0:
                    telex_line = convert_line_to_telex(line, telex_mapping)
                    telex_lines.append(telex_line)
                    temp_line_count -= 1
                else:
                    today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    print(f"Creating {OUTPUT_PATH}telex_output" + "_" + today + "_" + str(output_count) + "." + "txt")
                    with open(OUTPUT_PATH + "telex_output" + "_" + today + "_" + str(output_count) + "." + "txt", "w", encoding="utf-8") as f_out:
                        f_out.write("\n".join(telex_lines))
                    output_count += 1
                    temp_line_count = number_of_lines
                    telex_lines = []

                if output_count > OUTPUT_COUNT_LIMIT:
                    break
        return output_count

    except FileNotFoundError:
        sys.exit("Input file not found.")
    except Exception as e:
        sys.exit("An error occurred:", str(e))

def main():
    telex_mapping = TELEX_MAPPING

    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py <input_file> <number_of_lines>")
    else:
        input_file = sys.argv[1]
        number_of_lines = int(sys.argv[2])

    file_count = convert_multiple_lines_to_telex(input_file, telex_mapping, number_of_lines)
    print(f"{file_count - 1} files created successfully. Output written to {OUTPUT_PATH}.")



if __name__ == "__main__":
    main()
