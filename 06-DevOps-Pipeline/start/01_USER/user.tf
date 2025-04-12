/* **************************************************
resource "aws_iam_access_key" "confoo_github_actions" {
  user = aws_iam_user.confoo_github_actions.name
}

output "secret" {
  value = aws_iam_access_key.confoo_github_actions.encrypted_secret
}
************************************************** */


resource "aws_iam_user" "confoo_github_actions" {
  name = "confoo-github-actions"

  tags = {
    tag-key = "tag-value"
  }
}

data "aws_iam_policy_document" "s3_and_all" {
  statement {
    actions   = ["*"]
    resources = ["*"]
    effect    = "Allow"
  }
}

resource "aws_iam_user_policy" "confoo_github_actions" {
  name   = "github_actions"
  user   = aws_iam_user.confoo_github_actions.name
  policy = data.aws_iam_policy_document.s3_and_all.json
}