import FeatureExtractor

class FeatureExtractorCollection():
    extractor_dict = {}

    def __init__(self):
        self.__id_freq_extractor = FeatureExtractor.FeatureExtractorIDFrequency()
        self.__id_msg_extractor = FeatureExtractor.FeatureExtractorIDMsgFrequency()
        self.__data_len_extractor = FeatureExtractor.FeatureExtractorDataLength()
        self.__TAV_extractor = FeatureExtractor.FeatureExtractorTAV()
        self.__load_dict()

    def __load_dict(self):
        FeatureExtractorCollection.extractor_dict = {
            "FeatureCampaign": [self.__id_freq_extractor, self.__id_msg_extractor, self.__data_len_extractor],
            "ISOTPCampaign": [self.__id_freq_extractor]
        }

    def get_features(self, can_msg, campaign):
        extractor_chain = FeatureExtractorCollection.extractor_dict.get(campaign)
        feature_list = [extractor.extract_features(can_msg) for extractor in extractor_chain]
        return feature_list