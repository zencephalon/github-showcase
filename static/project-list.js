
function make_project_html(project) {
    var html = "<li class='repository'>";
    html += '<p>' + project + '</p>';
    html += '</li>';
}

$().ready(function() {
    var projects = ["Tekstfly", "Alphabet", "Mettacode"];
    for (i = 0; i < projects.size; i++) {
        var project = projects[i];
        alert('hello');
        $('#project-list').append(make_project_html(project));
    });
});
