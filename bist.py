import yfinance as yf
import pandas as pd
from telegram import Bot
import logging
import asyncio
from aiogram import Bot as AiogramBot
from dotenv import load_dotenv
load_dotenv()
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

bot_token = os.environ.get('bot_token')
chat_id = int(os.environ.get('chat_id'))

async def send_telegram_message(text):
    try:
        bot = AiogramBot(token=bot_token)
        await bot.send_message(chat_id=chat_id, text=text)
        logging.info("Telegram'a mesaj başarıyla gönderildi.")
    except Exception as e:
        logging.error(f"Mesaj gönderilemedi: {e}")

def get_stock_data(symbol, period='5y', interval='1wk'):
    try:
        data = yf.download(symbol + '.IS', period=period, interval=interval)
        if data.empty:
            logging.warning(f"{symbol} için veri bulunamadı.")
        else:
            logging.info(f"{symbol} için veri başarıyla alındı.")
        return data
    except Exception as e:
        logging.error(f"{symbol} için veri alma hatası: {e}")
        return pd.DataFrame()

def calculate_moving_averages(data, windows=[50, 100, 144]):
    averages = {}
    try:
        for window in windows:
            averages[f"SMA_{window}"] = data['Close'].rolling(window=window).mean()
        logging.info("Hareketli ortalamalar başarıyla hesaplandı.")
    except Exception as e:
        logging.error(f"Hareketli ortalamaları hesaplama hatası: {e}")
    return averages

def is_close_to_average(data, averages, symbol, tolerance=0.02):
    try:
        close_price = data['Close'].iloc[-1]
        for key, avg_series in averages.items():
            if not avg_series.empty:
                last_avg_value = avg_series.iloc[-1]
                if (abs(close_price - last_avg_value) / last_avg_value <= tolerance).all():
                    return  f"📈 *{symbol}* hissesinin {key.split('_')[1]} haftalık ortalamasına yakın olduğu tespit edildi!\n" \
                            f"💵 Kapanış fiyatı: {round(close_price.iloc[-1], 2)} TL,\n" \
                            f"📊 {key.split('_')[1]} haftalık ortalama fiyatı: {round(last_avg_value.iloc[-1], 2)} TL\n" \
                            f"📉 Ortalamaya uzaklık: %{round(((close_price.iloc[-1] - last_avg_value.iloc[-1]) / last_avg_value.iloc[-1]) * 100, 2)}"
        return None
    except Exception as e:
        logging.error(f"Kapanış fiyatını ortalamalarla karşılaştırma hatası: {e}")
        return None

async def main():
    symbols = ['BINHO', 'AVOD', 'A1CAP', 'ACSEL', 'ADEL', 'ADESE', 'ADGYO', 'AFYON', 'AGHOL', 'AGESA', 'AGROT', 'AHSGY', 'AHGAZ', 'AKBNK', 'AKCNS', 'AKYHO', 'AKENR', 'AKFGY', 'AKFYE', 'ATEKS', 'AKSGY', 'AKMGY', 'AKSA', 'AKSEN', 'AKGRT', 'AKSUE', 'AKTVK', 'AFB, AKTIF', 'ALCAR', 'ALGYO', 'ALARK', 'ALBRK, ALK', 'ALCTL', 'ALFAS', 'ALJF', 'ALKIM', 'ALKA', 'ALNUS, ANC', 'AYCES', 'ALTNY', 'ALKLC', 'ALMAD', 'ALVES', 'ANSGR', 'AEFES', 'ANHYT', 'ASUZU', 'ANGEN', 'ANELE', 'ARCLK', 'ARDYZ', 'ARENA', 'ARSAN', 'ARTMS', 'ARZUM', 'ASGYO', 'ASELS', 'ASTOR', 'ATAGY', 'ATA, ATAYM', 'ATAKP', 'AGYO', 'ATLFA', 'ATSYH', 'ATLAS', 'ATATP', 'AVGYO', 'AVTUR', 'AVHOL', 'AVPGY', 'AYDEM', 'AYEN', 'AYES', 'AYGAZ', 'AZTEK', 'BAGFS', 'BAHKM', 'BAKAB', 'BALAT', 'BNTAS', 'BANVT', 'BARMA', 'BASGZ', 'BASCM', 'BEGYO', 'BTCIM', 'BSOKE', 'BYDNR', 'BAYRK', 'BERA', 'BRKT', 'BRKSN', 'BJKAS', 'BEYAZ', 'BIENF', 'BIENY', 'BLCYT', 'BLKOM', 'BIMAS', 'BINBN', 'BIOEN', 'BRKVY', 'BRKO', 'BRLSM', 'BRMEN', 'BIZIM', 'BMSTL', 'BMSCH', 'BNPPI', 'BOBET', 'BORSK', 'BORLS', 'BRSAN', 'BRYAT', 'BFREN', 'BOSSA', 'BRISA', 'BURCE', 'BURVA', 'BUCIM', 'BVSAN', 'BIGCH', 'CRFSA', 'CASA', 'CEMZY', 'CEOEM', 'CCOLA', 'CONSE', 'COSMO', 'CRDFA', 'CVKMD', 'CWENE', 'CAGFA', 'CLDNM', 'CANTE', 'CATES', 'CLEBI', 'CELHA', 'CLKMT', 'CEMAS', 'CEMTS', 'CMBTN', 'CMENT', 'CIMSA', 'CUSAN', 'DYBNK', 'DAGI', 'DAGHL', 'DAPGM', 'DARDL', 'DGATE', 'DCTTR', 'DGRVK', 'DMSAS', 'DENGE', 'DENFA', 'DNFIN', 'DZGYO', 'DZY, DZYMK', 'DENIZ, DNZ', 'DERIM', 'DERHL', 'DESA', 'DESPC', 'DTBMK', 'DEVA', 'DNISI', 'DIRIT', 'DITAS', 'DMRGD', 'DOCO', 'DOFER', 'DOBUR', 'DOHOL', 'DTRND', 'DGNMO', 'ARASE', 'DOGUB', 'DGGYO', 'DOAS', 'DFKTR', 'DOKTA', 'DURDO', 'DURKN', 'DNYVA', 'DYOBY', 'EDATA', 'EBEBK', 'ECZYT', 'EDIP', 'EFORC', 'EGEEN', 'EGGUB', 'EGPRO', 'EGSER', 'EPLAS', 'ECILC', 'EKER', 'EKIZ', 'EKOFA', 'EKOS', 'EKOVR', 'EKSUN', 'ELITE', 'EMKEL', 'EMNIS', 'EMIRV', 'EKTVK', 'EKGYO', 'EMVAR', 'ENJSA', 'ENERY', 'ENKAI', 'ENSRI', 'ERBOS', 'ERCB', 'EREGL', 'ERGLI', 'KIMMR', 'ERSU', 'ESCAR', 'ESCOM', 'ESEN', 'ETILR', 'EUKYO', 'EUYO', 'ETYAT', 'EUHOL', 'TEZOL', 'EUREN', 'EUPWR', 'EYGYO', 'FADE', 'FSDAT', 'FMIZP', 'FENER', 'FBB, FBBNK', 'FLAP', 'FONET', 'FROTO', 'FORMT', 'FORTE', 'FRIGO', 'FZLGY', 'GWIND', 'GSRAY', 'GAPIN', 'GARFA', 'GRNYO', 'GEDIK', 'GEDZA', 'GLCVY', 'GENIL', 'GENTS', 'GEREL', 'GZNMI', 'GIPTA', 'GMTAS', 'GESAN', 'GLB, GLBMD', 'GLYHO', 'GGBVK', 'GSIPD', 'GOODY', 'GOKNR', 'GOLTS', 'GOZDE', 'GRTHO', 'GSDDE', 'GSDHO', 'GUBRF', 'GLRYH', 'GUNDG', 'GRSEL', 'SAHOL', 'HALKF', 'HLGYO', 'HLVKS', 'HALKI, HLY', 'HRKET', 'HATSN', 'HATEK', 'HDFFL', 'HDFGS', 'HEDEF', 'HDFVK', 'HDFYB, HYB', 'HEKTS', 'HEPFN', 'HKTM', 'HTTBT', 'HOROZ', 'HUBVC', 'HUNER', 'HUZFA', 'HURGZ', 'ENTRA', 'ICB, ICBCT', 'ICUGS', 'INGRM', 'INVEO', 'IAZ, INVAZ', 'INVES', 'ISKPL', 'IEYHO', 'IDGYO', 'IHEVA', 'IHLGM', 'IHGZT', 'IHAAS', 'IHLAS', 'IHYAY', 'IMASM', 'INALR', 'INDES', 'INFO, IYF', 'INTEK', 'INTEM', 'IPEKE', 'ISDMR', 'ISTFK', 'ISFAK', 'ISFIN', 'ISGYO', 'ISGSY', 'ISMEN, IYM', 'ISYAT', 'ISBIR', 'ISSEN', 'IZINV', 'IZENR', 'IZMDC', 'IZFAS', 'JANTS', 'KFEIN', 'KLKIM', 'KLSER', 'KLVKS', 'KAPTESTAS001, TRAKAPTEST01', 'KAPLM', 'KRDMA, KRDMB, KRDMD', 'KAREL', 'KARSN', 'KRTEK', 'KARYE', 'KARTN', 'KATVK', 'KTLEV', 'KATMR', 'KAYSE', 'KNTFA', 'KENT', 'KERVT', 'KRVGD', 'KERVN', 'TCKRC', 'KZBGY', 'KLGYO', 'KLRHO', 'KMPUR', 'KLMSN', 'KCAER', 'KFKTF', 'KOCFN', 'KCHOL', 'KOCMT', 'KLSYN', 'KNFRT', 'KONTR', 'KONYA', 'KONKA', 'KGYO', 'KORDS', 'KRPLS', 'KORTS', 'KOTON', 'KOZAL', 'KOZAA', 'KOPOL', 'KRGYO', 'KRSTL', 'KRONT', 'KTKVK', 'KSTUR', 'KUVVA', 'KUYAS', 'KBORU', 'KZGYO', 'KUTPO', 'KTSKR', 'LIDER', 'LIDFA', 'LILAK', 'LMKDC', 'LINK', 'LOGO', 'LKMNH', 'LRSHO', 'LUKSK', 'LYDHO', 'LYDYE', 'MACKO', 'MAKIM', 'MAKTK', 'MANAS', 'MRBAS, MRS', 'MAGEN', 'MRMAG', 'MARKA', 'MAALT', 'MRSHL', 'MRGYO', 'MARTI', 'MTRKS', 'MAVI', 'MZHLD', 'MEDTR', 'MEGMT', 'MEGAP', 'MEKAG', 'MEKMD, MSA', 'MNDRS', 'MEPET', 'MERCN', 'MRBKF', 'MBFTR', 'MERIT', 'MERKO', 'METUR', 'METRO', 'MTRYO', 'MHRGY', 'MIATK', 'MGROS', 'MSGYO', 'MPARK', 'MMCAS', 'MOBTL', 'MOGAN', 'MNDTR', 'EGEPO', 'NATEN', 'NTGAZ', 'NTHOL', 'NETAS', 'NIBAS', 'NUHCM', 'NUGYO', 'NRHOL', 'NRLIN', 'NURVK', 'NRBNK, NYB', 'OBAMS', 'OBASE', 'ODAS', 'ODINE', 'OFSYM', 'ONCSM', 'ONRYT', 'OPET', 'OPTMA', 'ORCAY', 'ORFIN', 'ORGE', 'ORMA', 'OMD, OSMEN', 'OSTIM', 'OTKAR', 'OTOKC', 'OTTO', 'OYAKC', 'OYA, OYYAT', 'OYAYO', 'OYLUM', 'OZKGY', 'OZATD', 'OZGYO', 'OZRDN', 'OZSUB', 'OZYSR', 'PAMEL', 'PNLSN', 'PAGYO', 'PAPIL', 'PRFFK', 'PRDGS', 'PRKME', 'PARSN', 'PBT, PBTR', 'PASEU', 'PSGYO', 'PATEK', 'PCILT', 'PGSUS', 'PEKGY', 'PENGD', 'PENTA', 'PEHOL', 'PSDTC', 'PETKM', 'PKENT', 'PETUN', 'PINSU', 'PNSUT', 'PKART', 'PLTUR', 'POLHO', 'POLTK', 'PRZMA', 'QYATB, YBQ', 'QYHOL', 'FIN, QNBTR', 'QNBFF', 'QNBFK', 'QNBVK', 'FNY, QNBIN', 'QUAGR', 'QUFIN', 'RNPOL', 'RALYH', 'RAYSG', 'REEDR', 'RYGYO', 'RYSAS', 'RODRG', 'ROYAL', 'RGYAS', 'RTALB', 'RUBNS', 'SAFKR', 'SANEL', 'SNICA', 'SANFM', 'SANKO', 'SAMAT', 'SARKY', 'SARTN', 'SASA', 'SAYAS', 'SDTTR', 'SEGMN', 'SEKUR', 'SELEC', 'SELGD', 'SELVA', 'SNKRN', 'SRVGY', 'KHSTR', 'SEYKM', 'SHTRP', 'SILVR', 'SNGYO', 'SKYLP', 'SMRTG', 'SMART', 'SODSN', 'SOKE', 'SKTAS', 'SONME', 'SNPAM', 'SUMAS', 'SUNTK', 'SURGY', 'SUWEN', 'SMRFA', 'SMRVA', 'SEKFA', 'SEKFK', 'SEGYO', 'SKY, SKYMD', 'SEK, SKBNK', 'SOKM', 'DRPHN', 'TOKI', 'TABGD', 'TAC, TCRYT', 'TAMFA', 'TNZTP', 'TARKM', 'TATGD', 'TATEN', 'TAVHL', 'TEBCE', 'TEKTU', 'TKFEN', 'TKNSA', 'TMPOL', 'TRFFA', 'TAE, TRBNK', 'TERA, TRA', 'TFNVK', 'TGSAS', 'TIMUR', 'TRYKI', 'TOASO', 'TRGYO', 'TLMAN', 'TSPOR', 'TDGYO', 'TRMEN, TVM', 'TSGYO', 'TUCLK', 'TUKAS', 'TRCAS', 'TUREX', 'MARBL', 'TRILC', 'TCELL', 'TMSN', 'TUPRS', 'THYAO', 'PRKAB', 'TTKOM', 'TTRAK', 'TBORG', 'TURGG', 'GARAN', 'HALKB', 'ISATR', 'ISBTR',' ISCTR',' ISKUR', 'KLNMA', 'TSKB', 'TURSG', 'SISE', 'UFUK', 'ULAS', 'ULUFA', 'ULUSE', 'ULUUN', 'UMPAS', 'USAK', 'ULKER', 'UNLU', 'VAKFN', 'VKGYO', 'VKFYO', 'VAKFK', 'VAKKO', 'VANGD', 'VBTYZ', 'VRGYO', 'VERUS', 'VERTU', 'VESBE', 'VESTL', 'VKING', 'YKFIN', 'YKBNK', 'YAPRK', 'YATAS', 'YYLGD', 'YAYLA', 'YGGYO', 'YEOTK', 'YGYO', 'YYAPI', 'YESIL', 'YBTAS', 'YIGIT', 'YONGA', 'YKSLN', 'YUNSA', 'ZEDUR', 'ZRGYO', 'ZOREN'];

    for symbol in symbols:
        data = get_stock_data(symbol)
        if data.empty:
            continue

        averages = calculate_moving_averages(data)
        message = is_close_to_average(data, averages, symbol=symbol)

        if message:
            await send_telegram_message(f"{message}")
        else:
            logging.info(f"{symbol}: Herhangi bir sinyal bulunamadı.")

if __name__ == "__main__":
    asyncio.run(main())
