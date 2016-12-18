$(document).ready(function() {
    d3.json('/static/micro/js/ufo-sightings.json', function(data) {
        MG.data_graphic({
            title: "UFO Sightings",
            description: "Yearly UFO sightings from the year 1945 to 2010.",
            // data: data,
            data: data,
            width: 650,
            height: 150,
            target: '#ufo-sightings',
            x_accessor: 'year',
            y_accessor: 'sightings',
            markers: [{
                'year': 1964,
                'label': '"The Creeping Terror" released'
            }]
        })
    })
})