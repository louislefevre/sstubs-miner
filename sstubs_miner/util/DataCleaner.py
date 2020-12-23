class DataCleaner:
    def __init__(self):
        pass

    def clean(self, sstubs):
        clean_sstubs = []
        for sstub in sstubs:
            self._add_missing_build(sstub)
            self._rename_build(sstub)

            if self._has_missing_values(sstub):
                continue
            clean_sstubs.append(sstub)
        return clean_sstubs

    @staticmethod
    def _add_missing_build(sstub):
        missing = DataCleaner._missing_builds()
        project_name = sstub.project_name
        build_system = sstub.build_system
        if not build_system:
            if project_name in missing:
                sstub.build_system = missing.get(project_name)
        return sstub

    @staticmethod
    def _rename_build(sstub):
        builds = {'Gradle': ['build.gradle', 'build.gradle.kts'],
                  'Bazel': ['build.bazel', 'build'],
                  'Maven': ['pom.xml'], 'Ant': ['build.xml'],
                  'Make': ['makefile'], 'None': ['none']}
        for build, build_files in builds.items():
            for build_file in build_files:
                if sstub.build_system == build_file:
                    sstub.build_system = build
                    return
        sstub.build_system = 'Other'

    @staticmethod
    def _has_missing_values(sstub):
        for value in sstub.__dict__.values():
            if not value:
                return True
        return False

    @staticmethod
    def _missing_builds():
        return {'FreeTymeKiyan/LeetCode-Sol-Res': 'none', 'Konloch/bytecode-viewer': 'none',
                'M66B/XPrivacy': 'build.gradle', 'Microsoft/malmo': 'cmakelists.txt', 'OpenGenus/cosmos': 'makefile',
                'TheAlgorithms/Java': 'none', 'alibaba/Dragonfly': 'dockerfile', 'alibaba/LuaViewSDK': 'build.gradle',
                'alibaba/atlas': 'build.gradle', 'apache/cassandra': 'build.xml',
                'apache/cordova-android': 'build.gradle',
                'apache/cordova-plugin-inappbrowser': 'none', 'apache/nutch': 'build.xml', 'apache/tomcat': 'build.xml',
                'commonsguy/cw-android': 'build.xml', 'commonsguy/cw-omnibus': 'build.gradle',
                'cryptomator/cryptomator': 'pom.xml', 'cymcsg/UltimateAndroid': 'build.gradle',
                'cymcsg/UltimateRecyclerView': 'build.gradle', 'facebook/buck': 'build.xml',
                'gitblit/gitblit': 'build.xml', 'google/android-classyshark': 'build.gradle', 'google/auto': 'pom.xml',
                'google/j2objc': 'makefile', 'google/physical-web': 'build.gradle',
                'googlemaps/android-samples': 'build.gradle',
                'googlesamples/android-architecture-components': 'build.gradle',
                'googlesamples/android-play-billing': 'build.gradle', 'googlesamples/google-services': 'build.gradle',
                'iSoron/uhabits': 'build.gradle', 'jitsi/jitsi': 'build.xml', 'jpush/aurora-imui': 'build.gradle',
                'katzer/cordova-plugin-local-notifications': 'none', 'lionsoul2014/ip2region': 'build.xml',
                'nathanmarz/storm': 'none', 'nicolasgramlich/AndEngine': 'build.xml',
                'phishman3579/java-algorithms-implementation': 'build.xml', 'qiujuer/Genius-Android': 'build.gradle',
                'react-community/react-native-image-picker': 'build.gradle', 'rzwitserloot/lombok': 'build.xml',
                'sherxon/AlgoDS': 'none', 'todoroo/astrid': 'build.xml', 'typesafehub/config': 'build.sbt',
                'uber/RIBs': 'build.gradle', 'wequick/Small': 'build.gradle', 'wingjay/jianshi': 'build.gradle',
                'yusugomori/DeepLearning': 'none', 'zmxv/react-native-sound': 'build.gradle',
                'zo0r/react-native-push-notification': 'build.gradle'}
