import json

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
    # this can be alt
    'ươ': 'uow', 'ướ': 'uows', 'ườ': 'uowf', 'ưở': 'uowr', 'ưỡ': 'uowx', 'ượ': 'uowj',
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


TELEX_MAPPING_MORE = {
    "single_vowel": {
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
    },
    "double_vowel": {
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
        # this can be alt
        'ươ': 'uow', 'ướ': 'uows', 'ườ': 'uowf', 'ưở': 'uowr', 'ưỡ': 'uowx', 'ượ': 'uowj',
    }
}


class VietVowelCluster:
    def __init__(self, main, mod=None, diacritics=None) -> None:
        self.main = main
        self.mod = mod
        self.diacritics = diacritics


def convert(mapping):
    single_vowel = mapping["double_vowel"]
    single_vowel_list = single_vowel.items()
    new_single_vowel_list = []
    for item in single_vowel_list:
        name = item[0]
        main = item[1][0:2]
        diacritics = item[1][-1]
        mod = item[1][2]
        new_vowel = {"name": name, "main": main,
                     "mod": mod, "diacritics": diacritics}
        new_single_vowel_list.append(new_vowel)
    new_single_vowel = {
        "single_vowel": new_single_vowel_list
    }
    # with open("temp.json", "w", encoding="utf-8") as f:
    #     f.write(json.dumps(new_single_vowel))
    print(new_single_vowel)


convert(TELEX_MAPPING_MORE)
