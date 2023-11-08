import sys

def convert_to_telex(vietnamese_text):
    telex_mapping = {
        'áu': 'aus', 'àu': 'auf', 'ảu': 'aur', 'ãu': 'aux', 'ạu': 'auj',
        'ái': 'ais', 'ài': 'aif', 'ải': 'air', 'ãi': 'aix', 'ại': 'aij',
        'áo': 'aos', 'ào': 'aof', 'ảo': 'aor', 'ão': 'aox', 'ạo': 'aoj',
        'áy': 'ays', 'ày': 'ayf', 'ảy': 'ayr', 'ãy': 'ayx', 'ạy': 'ayj',
        'ắu': 'awus', 'ằu': 'awuf', 'ẳu': 'awur', 'ẵu': 'awux', 'ặu': 'auj',
        'ắy': 'awys', 'ằy': 'awyf', 'ẳy': 'awyr', 'ẵy': 'awyx', 'ặy': 'ayj',
        'ấu': 'auas', 'ầu': 'auaf', 'ấu': 'auar', 'ẫu': 'auax', 'ậu': 'auaj',
        'ấy': 'ayas', 'ầy': 'ayaf', 'ấy': 'ayar', 'ẫy': 'ayax', 'ậy': 'ayaj',
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
        'á': 'as', 'à': 'af', 'ả': 'ar', 'ã': 'ax', 'ạ': 'aj', 'ắ': 'aws', 'ằ': 'awf', 'ẳ': 'awr', 'ẵ': 'awx', 'ặ': 'awj', 'ấ': 'asa', 'ầ': 'afa', 'ấ': 'ara', 'ẫ': 'axa', 'ậ': 'aja',
        'é': 'es', 'è': 'ef', 'ẻ': 'er', 'ẽ': 'ex', 'ẹ': 'ej', 'ế': 'ews', 'ề': 'ewf', 'ể': 'ewr', 'ễ': 'ewx', 'ệ': 'ewj',
        'í': 'is', 'ì': 'if', 'ỉ': 'ir', 'ĩ': 'ix', 'ị': 'ij',
        'ó': 'os', 'ò': 'of', 'ỏ': 'or', 'õ': 'ox', 'ọ': 'oj', 'ố': 'oso', 'ồ': 'ofo', 'ổ': 'oro', 'ỗ': 'oxo', 'ộ': 'ojo',
        'ớ': 'ows', 'ờ': 'owf', 'ở': 'owr', 'ỡ': 'owx', 'ợ': 'owj',
        'ú': 'us', 'ù': 'uf', 'ủ': 'ur', 'ũ': 'ux', 'ụ': 'uj', 'ứ': 'uws', 'ừ': 'uwf', 'ử': 'uwr', 'ữ': 'uwx', 'ự': 'uwj',
        'ý': 'ys', 'ỳ': 'yf', 'ỷ': 'yr', 'ỹ': 'yx', 'ỵ': 'yj',
        'đ': 'dd'
    }

    words = vietnamese_text.split()  # Split input text into words
    telex_words = []

    for word in words:
        telex_word = ''
        i = 0
        word_len = len(word)

        while i < word_len:
            found = False

            # Try to find multi-character combinations in decreasing order of length
            for j in range(min(5, word_len - i), 1, -1):
                subword = word[i:i+j]
                if subword in telex_mapping:
                    telex_word += telex_mapping[subword]
                    i += j
                    found = True
                    break

            if not found:
                telex_word += word[i]
                i += 1

        telex_words.append(telex_word)

    return ' '.join(telex_words)

def main(input_file, output_file):
    try:
        # Read input text file
        with open(input_file, "r", encoding="utf-8") as f:
            input_content = f.read()

        # Split input content into words and convert Vietnamese to English
        # words = input_content.split()
        # processed_words = [convert_to_telex(word) for word in words]

        # Join processed words back into a string
        # processed_content = " ".join(processed_words)

        # Write processed content to output text file
        with open(output_file, "w", encoding="utf-8") as f:
            # f.write(processed_content)
            f.write(convert_to_telex(input_content))

        print("Output written to", output_file)

    except FileNotFoundError:
        print("Input file not found.")
    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python program_name.py <input_file> <output_file>")
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
        main(input_file, output_file)
