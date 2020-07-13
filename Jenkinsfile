label = "${UUID.randomUUID().toString()}"
git_project = "nuclio-templates"
git_project_user = "nuclio"
git_project_upstream_user = "nuclio"
git_deploy_user = "iguazio-prod-git-user"
git_deploy_user_token = "iguazio-prod-git-user-token"
git_deploy_user_private_key = "iguazio-prod-git-user-private-key"

podTemplate(label: "${git_project}-${label}", inheritFrom: "jnlp-docker") {
    node("${git_project}-${label}") {
        pipelinex = library(identifier: 'pipelinex@development', retriever: modernSCM(
                [$class       : 'GitSCMSource',
                 credentialsId: git_deploy_user_private_key,
                 remote       : "git@github.com:iguazio/pipelinex.git"])).com.iguazio.pipelinex
        common.notify_slack {
            withCredentials([
                    string(credentialsId: git_deploy_user_token, variable: 'GIT_TOKEN')
            ]) {
                github.release(git_deploy_user, git_project, git_project_user, git_project_upstream_user, true, GIT_TOKEN) {
                    stage("upload ${git_project} zip to artifactory") {
                        container('jnlp') {
                            sh("wget https://github.com/${git_project_user}/${git_project}/archive/${github.TAG_VERSION}.zip")

                            zip_path = sh(
                                    script: "pwd",
                                    returnStdout: true
                            ).trim()

                            withCredentials([
                                    string(credentialsId: pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[2], variable: 'PACKAGES_ARTIFACTORY_PASSWORD')
                            ]) {
                                common.upload_file_to_artifactory(pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[0], pipelinex.PackagesRepo.ARTIFACTORY_IGUAZIO[1], PACKAGES_ARTIFACTORY_PASSWORD, "iguazio-devops/nuclio-templates", "${github.TAG_VERSION}.zip", zip_path)
                            }
                        }
                    }
                }
            }
        }
    }
}
