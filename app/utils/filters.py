def format_indonesian_date(date):
    if not date:
        return '-'
        
    MONTHS_IN_INDONESIAN = {
        'January': 'Januari',
        'February': 'Februari',
        'March': 'Maret',
        'April': 'April',
        'May': 'Mei',
        'June': 'Juni',
        'July': 'Juli',
        'August': 'Agustus',
        'September': 'September',
        'October': 'Oktober',
        'November': 'November',
        'December': 'Desember'
    }
    
    english_date = date.strftime('%d %B %Y')
    for eng, ind in MONTHS_IN_INDONESIAN.items():
        if eng in english_date:
            return english_date.replace(eng, ind)
    return english_date

__all__ = ['format_indonesian_date']