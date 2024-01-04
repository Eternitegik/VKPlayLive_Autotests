from src import WDWait
import pytest
import Config


class TestCategories:
    @pytest.mark.parametrize(
        ('Cat_url', 'Cat_text'),
        [
            ('categories', 'Популярные'),
            ('categories/newest', 'Недавние релизы'),
        ]
    )
    def test_CatalogCategories(self, setup, Cat_url, Cat_text):
        '''101 | Проверка списка игр'''
        print(f'{Config.MAINPAGEURL}/{Cat_url}')
        setup.get(f'{Config.MAINPAGEURL}/{Cat_url}')

        print(f'Страница "{Cat_text}"')
        el = WDWait.VisibilityElement(
            setup, '//div[contains(@class, "CatalogCategories_title")]', 'Не найдено поле для надписи')
        assert el.text == Cat_text

        print('Список игр не пуст')
        WDWait.AssertVisibilityElement_s(
            setup, '//a[contains(@class, "CatalogCategory_root")]', 'Не найдены карточки игр')

        setup.find_element(
            'xpath', '//button[contains(@class, "CatalogCategories_back")]').click()

    @pytest.mark.parametrize(
        ('Cat_url', 'Cat_text'),
        [
            ('streams/often', 'Часто стримят'),
            ('streams/cozy', 'Ламповый поток'),
            ('streams/all', 'Сейчас в эфире'),
        ]
    )
    def test_CatalogStreams(self, setup, Cat_url, Cat_text):
        '''102 | Проверка списка стримеров'''
        setup.get(f'{Config.MAINPAGEURL}/{Cat_url}')

        print(f'Страница "{Cat_text}"')
        el = WDWait.VisibilityElement(
            setup, '//div[contains(@class, "CatalogStreams_title")]', 'Не найдено поле для надписи')
        assert el.text == Cat_text

        print('Список игр не пуст')
        cat_id = WDWait.VisibilityElement_s(
            setup, '//span[contains(@class, "CatalogStream_container")]', 'Не найдены карточки игр')
        text = cat_id[0].get_property('id')

        assert text != ''

        setup.find_element(
            'xpath', '//button[contains(@class, "CatalogPreset_backLink")]').click()
