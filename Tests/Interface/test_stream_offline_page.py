from src import WDWait
import pytest
import Config


class TestStream:
    def test_open_stream_page(self, StreamPage):
        '''201 | Проверка открытия страницы стримера и наличие имени'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_author") and @title]', 'Поле с текстом не найдено')

        assert elem.text != '' or elem.text != None, 'Поле для текста пусто'
        assert elem.text in StreamPage.title, 'В заголовке страницы нет имени стримера'

    def test_streamer_avatar(self, StreamPage):
        '''202 | Проверка аватара'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//div[contains(@class, "Avatar_block")]/img', 'Не найден элемент для аватара')
        print('- url: ', elem.get_property('src'))
        assert elem.get_property('src') != '', 'Нет ссылки аватара'

    def test_streamer_number_subscribers(self, StreamPage):
        '''203 | Проверка надписи о количестве подписчиков'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//div[contains(@class, "StreamPanel_subscribers")]', 'Не найден элемент для надписи')

        assert 'подписчиков' in elem.text or 'подписчик' in elem.text, 'Нет надписи'

    def test_streamer_stream_title(self, StreamPage):
        '''204 | Проверка наличия описания стрима'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//div[contains(@class, "StreamPanel_title")]', 'Не найден элемент описания')

        assert elem.text != '', 'Элемент для описания пуст'

    def test_streamer_last_stream_text(self, StreamPage):
        '''205 | Проверка наличия надписи "Последний стрим..."'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//span[contains(@class, "LastStreamInfo_text")]', 'Поле для надписи не найдено')

        assert 'Последний стрим' in elem.text, 'Не найден текст'

    def test_streamer_category(self, StreamPage):
        '''206 | Проверка наличия кнопки с категорией'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//a[contains(@class, "StreamPanel_category")]', 'Не найден элемент с кнопкой')

        print('Текст кнопки не пуст')
        assert elem.text != "", 'Кнопка без текста'
        print('Проверка наличия url')
        print("-url: ", elem.get_property('href'))
        assert elem.get_property('href') != '', 'Не заполнен url кнопки'

    def test_streamer_follow_button(self, StreamPage):
        '''207 | Проверка наличия кнопки "Отслеживать"'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//button[contains(@class, "FollowButton_root")]', 'Не найден элемент с кнопкой')

        assert 'Отслеживать' in elem.text, 'Неправильный текст кнопки'

    def test_streamer_subscribe_button(self, StreamPage):
        '''208 | Проверка наличия кнопки "Подписаться"'''

        elem = WDWait.VisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//button[contains(@class, "SubscribeButtonBase_subscribe")]', 'Не найден элемент с кнопкой')

        assert 'ПОДПИСАТЬСЯ' in elem.text, 'Неправильный текст кнопки'

    def test_streamer_cinema_mode(self, StreamPage):
        '''209 | Проверка наличия кнопки "Режим кинотеатра"'''

        WDWait.AssertVisibilityElement(
            StreamPage, '//div[contains(@class, "StreamPanel_root")]//div[contains(@class, "StreamFooter_theatreButton")]//span', 'Не найден элемент с кнопкой')

    # @pytest.mark.skip('Доделать проверка на кнопку "Поделиться"')
    # def test_streamer_share(self, StreamPage):
    #     '''210 | Проверка наличия кнопки "Поделиться"'''

    #     elem = WDWait.VisibilityElement(
    #         StreamPage, '//div[contains(@class, "StreamPanel_root")]//span[contains(@class, "ShareDropdown_dropdownButtonIcon")]')

    #     assert elem
