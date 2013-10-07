var projects = ["Tekstfly", "Alphabet", "Mettacode"];

function make_project_html(project) {
    var html = "<li class='repository'>";
    html += '<p>' + project + '</p>';
    html += '</li>';
}

$().ready(function() {
    for each (project in projects) {
        $('#project-list').append(make_project_html(project))
    }
});
