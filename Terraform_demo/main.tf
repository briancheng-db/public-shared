data "databricks_current_user" "me" {
}

resource "databricks_notebook" "select_sql" {
  source = "sql.py"
  path   = "${data.databricks_current_user.me.home}/AA/notebook/sql2"
}


resource "databricks_job" "this" {
  name        = "Job with simple task"
  description = " "

  task {
    task_key = "a"

    notebook_task {
      notebook_path = databricks_notebook.select_sql.path
    }
  }

}