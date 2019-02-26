label = "${UUID.randomUUID().toString()}"
expired=240
git_project = "nuclio-templates"
git_project_user = "gkirok"
git_deploy_user_token = "iguazio-dev-git-user-token"
git_deploy_user_private_key = "iguazio-dev-git-user-private-key"

podTemplate(label: "${git_project}-${label}", inheritFrom: "jnlp-docker") {
    node("${git_project}-${label}") {
        withCredentials([
                string(credentialsId: git_deploy_user_token, variable: 'GIT_TOKEN')
        ]) {
            def TAG_VERSION
            pipelinex = library(identifier: 'pipelinex@DEVOPS-204-pipelinex', retriever: modernSCM(
                    [$class: 'GitSCMSource',
                     credentialsId: git_deploy_user_private_key,
                     remote: "git@github.com:iguazio/pipelinex.git"])).com.iguazio.pipelinex

            common.notify_slack {
                stage('get tag data') {
                    container('jnlp') {
                        TAG_VERSION = github.get_tag_version(TAG_NAME)
                        PUBLISHED_BEFORE = github.get_tag_published_before(git_project, git_project_user, "${TAG_VERSION}", GIT_TOKEN)

                        echo "$TAG_VERSION"
                        echo "$PUBLISHED_BEFORE"
                    }
                }

                if (TAG_VERSION != null && TAG_VERSION.length() > 0 && PUBLISHED_BEFORE < expired) {
                    parallel(
                            'source archive': {
                                container('jnlp') {
                                    sh("wget https://github.com/${git_project_user}/${git_project}/archive/${TAG_VERSION}.zip")

                                    zip_path = sh(
                                            script: "pwd",
                                            returnStdout: true
                                    ).trim()

                                    withCredentials([
                                            string(credentialsId: pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[2], variable: 'PACKAGES_ARTIFACTORY_PASSWORD')
                                    ]) {
                                        common.upload_file_to_artifactory(pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[0], pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[1], PACKAGES_ARTIFACTORY_PASSWORD, "iguazio-devops/nuclio-templates", "${TAG_VERSION}.zip", zip_path)
                                    }
                                }
                            }
                    )

                    stage('update release status') {
                        container('jnlp') {
                            github.update_release_status(git_project, git_project_user, "${TAG_VERSION}", GIT_TOKEN)
                        }
                    }
                } else {
                    stage('warning') {
                        if (PUBLISHED_BEFORE >= expired) {
                            currentBuild.result = 'ABORTED'
                            error("Tag too old, published before $PUBLISHED_BEFORE minutes.")
                        } else {
                            currentBuild.result = 'ABORTED'
                            error("${TAG_VERSION} is not release tag.")
                        }
                    }
                }
            }
        }
    }
}
