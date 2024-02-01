from src import WDWait
import pytest
import Config


class TestCheckPage:
    @pytest.fixture(scope='class')
    def StartPage(self, setup):
        setup.get(Config.MAINPAGEURL)
        return setup

    def test_main_page(self, StartPage):
        '''001 | Проверка заголовка главной страницы'''
        assert StartPage.title == 'VK Play Live - новый горизонт стриминга', 'Не верный заголовок для главной страницы'

    def test_PopupContent(self, StartPage):
        '''002 | Проверка отображения попапа с планами и обновлениями'''
        WDWait.AssertVisibilityElement(
            StartPage, '//div[contains(@class, "PopupContent_content")]', 'Нет попапа для планов и обновлений')

        StartPage.find_element(
            'xpath', '//span[contains(@class, "PopupContent_close") and contains(@class, "NewsPopup_close")]').click()

    def test_RecommendationTechnologiesAlert(self, StartPage):
        '''003 | Проверка отображения попапа "...рекомендательные технологии..."'''
        WDWait.AssertVisibilityElement(
            StartPage, '//div[contains(@class,"RecommendationTechnologiesAlert_root")]', 'Нет попапа "...рекомендательные технологии..."')


class TestCheckTopButton:

    def test_btn_vkPlayLive(self, MainPage):
        '''004 | Проверка кнопки "VK Play Live" в шапке'''
        WDWait.AssertVisibilityElement(
            MainPage, '//a[contains(@class, "TopMenu") and @href="/"]', 'Не найдена кнопка "VK Play Live"')

    @pytest.mark.parametrize(
        ('btn_name', 'btn_url'),
        [
            ('Игры', 'https://vkplay.ru/play/'),
            ('Библиотека', 'https://vkplay.ru/play/my/'),
            ('Live', 'https://vkplay.live'),
            ('Турниры', 'https://pvp.vkplay.ru/'),
            ('Медиа', 'https://media.vkplay.ru/'),
            ('Торговая площадка', 'https://market.vkplay.ru/'),
        ]
    )
    def test_head_btn(self, MainPage, btn_name, btn_url):
        '''005 | Проверка кнопок в шапке'''
        print(f'Наличие кнопки "{btn_name}"')
        print(f'c url: "{btn_url}"')
        elem = WDWait.VisibilityElement(
            MainPage, f'//a[contains(@class, "Links_item") and @href="{btn_url}"]', f'Не найдена кнопка "{btn_name}"')
        assert btn_name in elem.text, f'Не правильный текст для кнопки "{
            btn_name}"'

    def test_btn_support(self, MainPage):
        '''006 | Наличие кнопки техподдержки в шапке'''
        WDWait.AssertVisibilityElement(
            MainPage, '//a[contains(@class, "TopMenu_support") and @href="https://support.vkplay.ru/vkp_live"]', 'Кнопка "Техподдержка" не найдена')

    def test_btn_notifications(self, MainPage):
        '''007 | Наличие кнопки уведомлений в шапке'''
        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class, "News_root")]/span', 'Кнопка "Уведомления" не найдена')

    def test_btn_signIn(self, MainPage):
        '''008 | Наличие кнопки входа в шапке'''
        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class,"TopMenuRightUnAuthorized_signIn")]', 'Кнопка "Вход" не найдена')


class TestRecommendation:

    def test_recommendations(self, MainPage):
        '''009 | Проверка наличия блока рекомендаций'''
        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class,"Drawer_root_Id")]')

    def test_recommendations_roll(self, MainPage):
        '''010 | Наличие надписи "РЕКОМЕНДУЕМ" в блоке рекомендаций'''
        elem = WDWait.VisibilityElement(
            MainPage, '//div[contains(@class,"ScrollableComponent_container")]/div[contains(@class, "Channels_title")]', 'Поле для надписи не найдено')
        assert 'РЕКОМЕНДУЕМ' in elem.text, 'Неверный текст заголовка "РЕКОМЕНДУЕМ"'

    def test_recommendations_roll(self, MainPage):
        '''011 | Проверка кнопки сворачивания рекомендациях'''
        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class,"Drawer_root_Id")]/button[contains(@class, "BaseButton_button")]', 'Нет кнопки сворачивания')

    def test_recommendations_portal(self, MainPage):
        '''012 | Наличие кнопки "Портал" в рекомендациях'''
        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class,"Drawer_root_Id")]//button[contains(@class, "PortalButton_portalButton")]', 'Нет кнопки "Портал"')

    def test_recommendations_not_null(self, MainPage):
        '''013 | Проверка что блок рекомендаций не пуст'''
        elem = WDWait.VisibilityElement_s(
            MainPage, '//div[contains(@class,"Drawer_root_Id")]//button[contains(@class, "PortalButton_portalButton")]')
        assert len(elem) > 0, 'В блоке рекомендаций пусто'


class TestSearch:

    def test_check_search(self, MainPage):
        '''014 | Работа поиска '''
        elem_search = WDWait.VisibilityElement(
            MainPage, '//input[contains(@class, "SearchInputView")]', 'Блок поиска не найден')

        elem_search.click()
        elem_search.send_keys("eijk")

        WDWait.AssertVisibilityElement(
            MainPage, '//div[contains(@class, "SearchInput_suggestContainer")]', 'Не найден блок с результатами поиска')

        elem = WDWait.VisibilityElement_s(
            MainPage, '//div[contains(@class, "SearchInput_suggestContainer")]//div[contains(@class, "Input_notFound")]', 'Не отображается блок с результатами поиска')

        t = 'По запросу ничего не найдено.'
        print(f'Надпись "{t}" в блоке результатов поиска')
        assert t in elem[1].text, f'Не отображается надпись "{t}"'

        t = 'Убедитесь, что все слова написаны правильно, или попробуйте изменить запрос.'
        print(f'Надпись "{t}" в блоке результатов поиска')
        assert t in elem[2].text, f'Не отображается надпись "{t}"'

        elem_search.clear()
        elem_search.send_keys('ejik')

        elem = WDWait.VisibilityElement_s(
            MainPage, '//div[contains(@class, "SearchInput_suggestContainer")]//div[contains(@class, "Input_suggestItem")]', 'Не отображается блок с результатами поиска')
        print('Когда поиск дал результаты и блок не равен 0')
        assert len(elem) > 0, 'В блоке поиска пусто'

        elem_search.clear()


class TestCatalogShowcase:

    @pytest.mark.parametrize(
        ('btn_name', 'btn_xpath'),
        [
            ('Все', '//li[contains(@class, "StreamCategoryTypeSelector_item") and text()="Все"]'),
            ('Видеоигры',
             '//li[contains(@class, "StreamCategoryTypeSelector_item") and text()="Видеоигры"]'),
            ('Лайфстайл',
             '//li[contains(@class, "StreamCategoryTypeSelector_item") and text()="Лайфстайл"]'),
            ('Портал', '//div[contains(@class, "CategorySelector_root")]//button[contains(@class, "PortalButton_portalButton")]'),
            ('Предыдущий объект карусели',
             '//div[contains(@class, "CatalogShowcase_container")]//div[contains(@class, "CatalogShowcase_showPreviousButton")]'),
            ('Следующий объект карусели',
             '//div[contains(@class, "CatalogShowcase_container")]//div[contains(@class, "CatalogShowcase_showNextButton")]'),
        ]
    )
    def test_CatalogShowcase_btn(self, MainPage, btn_name, btn_xpath):
        '''015 | Блок карусели с предпросмотром'''

        print(f'Наличе кнопки "{btn_name}"')
        WDWait.AssertVisibilityElement(
            MainPage, btn_xpath, f'Нет кнопки "{btn_name}"')

    def test_CatalogShowcase_not_null(self, MainPage):
        '''016 | Блок карусели с предпросмотром не пуст'''

        elem = WDWait.PresenceElement_s(
            MainPage, '//div[contains(@class, "CatalogShowcase_list")]//div[contains(@class, "CatalogShowcaseStream_container")]', '')
        print('Проверка что в карусели есть объекты')
        assert len(elem) > 0, 'В карусели нет объектов стримов'


class TestCategories:

    @pytest.mark.parametrize(
        ('Cat_name', 'Cat_xpath'),
        [
            ('Популярные',
             '(//div[contains(@class, "CatalogCategoriesLayout_list")])[1]/child::a'),
            ('Недавние релизы',
             '(//div[contains(@class, "CatalogCategoriesLayout_list")])[2]/child::a'),
            ('Часто стримят',
             '(//div[contains(@class, "CatalogVideoLayout_list")])[1]'),
            ('Ламповый поток',
             '(//div[contains(@class, "CatalogVideoLayout_list")])[2]'),
            ('Сейчас в эфире',
             '(//div[contains(@class, "CatalogVideoLayout_list")])[3]'),
        ]
    )
    def test_Categories(self, MainPage, Cat_name, Cat_xpath):
        '''017 | Проверка категорий '''

        print(f'Проверка что блок "{Cat_name}" не пуст')
        assert len(WDWait.VisibilityElement_s(
            MainPage, Cat_xpath)) > 0, f'В блоке "{Cat_name}" ничего нет'


class TestFooter:
    @pytest.mark.parametrize(
        ('btn_text', 'btn_url', 'btn_xpath'),
        [
            ('Пользовательское соглашение', 'https://documentation.vkplay.ru/terms_vkp/tou_vkp',
             '//div[contains(@class, "Footer_links")]/a[1]'),
            ('Политика конфиденциальности', 'https://documentation.vkplay.ru/terms_vkp/privacy_vkp',
             '//div[contains(@class, "Footer_links")]/a[2]'),
            ('Поддержка', 'https://support.vkplay.ru/',
             '//div[contains(@class, "Footer_links")]/a[4]'),
        ]
    )
    def test_footer(self, MainPage, btn_text, btn_url, btn_xpath):
        '''018 | Проверка кнопок в футере'''

        print(f'Проверка наличие кнопки "{btn_text}"')
        elem = WDWait.VisibilityElement(
            MainPage, btn_xpath, f'Не найдена кнопка "{btn_text}"')

        assert btn_text in elem.text, f'Не тот текст у кнопки "{btn_text}"'
        print(f'Проверка ссылки у кнопки "{btn_text}"')
        assert btn_url in elem.get_attribute(
            'href'), f'Не правильный ulr у кнопки "{btn_text}"'
