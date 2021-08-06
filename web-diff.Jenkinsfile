node('web') {
    try {
        pipeline()
        success()
    } catch (e) {
        failure(e)
        throw e
    } finally {
        def currentResult = currentBuild.result ?: 'SUCCESS'
        if (currentResult == 'UNSTABLE') {
            unstable()
        }
        def previousResult = currentBuild.previousBuild?.result
        if (previousResult != null && previousResult != currentResult) {
            changed()
        }
        always()
    }
}

def pipeline() {
    def APPS = []
    def BUILDRESULTS
    def TAGS = [:]

    stage('print diff') {
        sh """
        git --no-pager diff --name-only HEAD^1 HEAD
        """
    }
    stage('diff to array') {
        def DIFF = sh(script: 'git --no-pager diff --name-only HEAD^1 HEAD',
                      returnStdout: true).trim()
        DIFF = DIFF.split('\n')
        DIFF.each { APP ->
            if (APP.startsWith('src/apps/a/')) {
                APPS.add("a")
            } else if (APP.startsWith('src/apps/b/')) {
                APPS.add("b")
            } else if (APP.startsWith('src/apps/c/')) {
                APPS.add("c")
            } else {
                APPS = ["a", "b", "c"]
            }
        }
    }
    stage('trigger builder') {
        def BUILDS = [:]
        APPS = APPS.toSet()
        APPS.each{ APP ->
            BUILDS["${APP}"] = {
                build job: "web/web-${APP}", parameters: [
                    string(name: 'TENANT', value: APP),
                ]
            }
        }
        BUILDRESULTS = parallel BUILDS
    }
    stage('build results') {
        BUILDRESULTS.keySet().each { APP ->
            def BUILD_NAME = BUILDRESULTS["${APP}"].projectName
            def BUILD_TAG = BUILDRESULTS["${APP}"].number.toString()
            BUILD_NAME = BUILD_NAME.split('web-')[-1]
            BUILD_TAG = "1.0." + BUILD_TAG
            TAGS.put("${BUILD_NAME}","${BUILD_TAG}")
        }
    }
    stage('deploy to pre-release') {
        def IMAGES = ""
        TAGS.each { TENANT, TAG ->
            IMAGES += "web/${TENANT}:${TAG}-rc "
        }
        build wait: false, job: 'pre/web-release', parameters: [
            string(name: 'IMAGES', value: IMAGES),
        ]
    }
}

def failure(e) {
    echo "error ${e}"
    telegramSend(message: "${env.JOB_NAME} has failed because ${e}\nSee ${env.BUILD_URL}console", chatId: "${env.TG_CHAT_ID}")
}

def success() {
    echo "success"
}

def unstable() {
    echo 'This will run only if the run was marked as unstable'
}

def changed() {
    echo 'This will run only if the state of the Pipeline has changed'
    echo 'For example, if the Pipeline was previously failing but is now successful'
}
