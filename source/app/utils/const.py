from enum import Enum


class methods(Enum):
    @classmethod
    def unique_id(cls):
        return list(map(lambda c: c.value[0], cls))
    @classmethod
    def base(cls):
        return list(map(lambda c: c.value[1], cls))
    @classmethod
    def code(cls):
        return list(map(lambda c: c.value[2], cls))
    @classmethod
    def color(cls):
        return list(map(lambda c: c.value[3], cls))
    @classmethod
    def name(cls):
        return list(map(lambda c: c.value[4], cls))
    
    @classmethod
    def code_color(cls):
        return list(map(lambda c: c.value[5], cls))


class bases(methods):
    water           = 0, '', '', '', 'Вода'
    green           = 1, '', '', '', 'Растительность'
    surface         = 2, '', '', '', 'Площадные объекты'
    infrastructure  = 3, '', '', '', 'Объекты и сооружения'


class classes(methods):
    #name = unique id, base, class number, globalcolor id [6-18], text description, code color
    c100 = 0,   0, 100, 6,  "Базовый Вода",                                                                 '#c0c0c0'
    c110 = 1,   0, 110, 7,  "Река, канал",                                                                  '#ff0000'
    c120 = 2,   0, 120, 8,  "Озеро, пруд, водохранилище",                                                   '#00ff00'
    c130 = 3,   0, 130, 9,  "Болото, рисовое поле",                                                         '#0000ff'
    c140 = 4,   0, 140, 10, "Океан, море",                                                                  '#00ffff'
 
    c200 = 5,   1, 200, 11,  "Базовый Растительность",                                                      '#ff00ff'
    c210 = 6,   1, 210, 12,  "Заросли кустарников и прочей низкой растительности (в т.ч. луга и степи)",    '#ffff00' 
    c220 = 7,   1, 220, 13,  "Редкий лесной массив (редко стоящие деревья)",                                '#800000'
    c230 = 8,   1, 230, 14, "Лесной массив (в т. ч. густые массивы)",                                       '#008000'
 
    c300 = 9,   2, 300, 15, "Базовый Площадные объекты",                                                    '#000080'
    c310 = 10,  2, 310, 16, "Город или другой населенный пункт",                                            '#008080'
    c320 = 11,  2, 320, 17, "Промышленное предприятие неопределённого типа",                                '#800080'
    c321 = 12,  2, 321, 18, "Порт",                                                                         '#808000'
    c322 = 13,  2, 322, 6, "Эл. Станция",                                                                   '#c0c0c0'
    c323 = 14,  2, 323, 7, "НПЗ",                                                                           '#ff0000'
    c350 = 15,  2, 350, 8, "Пески",                                                                         '#00ff00'

    c400 = 16,  3, 400, 9, "Базовый Объекты и сооружения",                                                  '#0000ff'
    с401 = 17,  3, 401, 10,  "Объект неопределенного типа",                                                 '#00ffff'
    c410 = 18,  3, 410, 11,  "Плотина, дамба",                                                              '#ff00ff'
    с411 = 19,  3, 411, 12,  "Мост",                                                                        '#ffff00'
    c420 = 20,  3, 420, 13,  "Автомобильная дорога",                                                        '#800000'
    с421 = 21,  3, 421, 14,  "Железная дорога",                                                             '#008000'
    c430 = 22,  3, 430, 15,  "Линия эл. передач",                                                           '#000080'
    c440 = 23,  3, 440, 16,  "Скалы",                                                                       '#008080'
    с441 = 24,  3, 441, 17,  "Террикон, отвал, насыпь, курган",                                             '#800080'
    c450 = 25,  3, 450, 18, "Здание неопределенного типа",                                                  '#808000'
    с451 = 26,  3, 451, 6, "Жилое строение",                                                                '#c0c0c0'
    с452 = 27,  3, 452, 7, "Промышленное строение или сооружение",                                          '#ff0000'
    с453 = 28,  3, 453, 8, "Причал",                                                                        '#00ff00'
    с454 = 29,  3, 454, 9, "Культурные и религиозные здания и сооружения",                                  '#0000ff'
    с455 = 30,  3, 455, 10, "Склад",                                                                        '#00ffff'
    с456 = 31,  3, 456, 11, "Склад горючего",                                                               '#ff00ff'
    с460 = 32,  3, 460, 12, "Аэродром",                                                                     '#ffff00'
    с461 = 33,  3, 461, 13, "Портовые сооружения и краны",                                                  '#800000'
    с490 = 34,  3, 490, 14,  "Особые здания",                                                               '#008000'

class hdfs(Enum):
    POSTFIX     = '.hdf5'
    NAME        = '__name__'
    CLASSES     = '__classes__'
    TIME_C      = '__time_created__'
    TIME_U      = '__time_updated__'
    DESCRIPTION = '__description__'
    TASK_COUNT  = '__task_count__'
    DONE_COUNT = '__done_count__'
    TO_CHECK_COUNT = '__to_check_count__'
    REQUIREMENTS = '__requirements__' 

class tasks(Enum):
    FILE_NAME   = '__file_name__'
    WIDTH       = '__width__'
    HEIGHT      = '__height__'
    COUNT       = '__polygon_count__'
    LAYERS_COUNT= '__layers_count__'
    STATUS      = '__task_status__'
    LEFT        = '__tasks_left__'
    RIGHT       = '__tasks_right__'
    TO_DO       = '__0__' #при создании файла проекта, при добавлении задачи
    IN_PROGRESS = '__1__' #у задачи есть хотя бы один атрибут маски
    TO_CHECK    = '__2__' #нажата кнопка отправить на проверку
    DONE        = '__3__' #модератор нажал кнопку 


class aerial(Enum):
    SOURCE      = '__aerial_device(txt)__'
    ALTITUDE    = '__altitude(km)__'
    LATITUDE    = '__latitude_top_left_point(xx:yy:zz)__'
    LONGITUDE   = '__longitude_top_left_point(xx:yy:zz)__'
    SUN         = '__sun_azimuth(xx:yy:zz)__'

    SPATIAL     = '__resolution(metres:pixel)__'
    SIZE        = '__pixels(width:height)__'

    DATE        = '__date_stamp(dd:mm:yy)__'
    TIME        = '__time_stamp(hh:mm)__'



class path(Enum):
    PROJECTS_FOLDER = 'projects'
    UPLOAD_FOLDER   = 'uploads'
    LOGS_FOLDER     = 'logs'
