import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:google_maps_flutter/google_maps_flutter.dart';

String url = r'https://api.jsonbin.io/b/5e893acd8841e979d0fde1db';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        primarySwatch: Colors.blueGrey,
      ),
      home: MyHomePage(title: 'Covid-19 denger spots'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);
  final String title;
  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  GoogleMapController _controller;
  BitmapDescriptor myIcon;
  Set<Marker> markers = Set();
  var day = 1.0;
  var hour = 15.0;

  @override
  Future<void> initState() {
    BitmapDescriptor.fromAssetImage(
        ImageConfiguration(devicePixelRatio: 200), 'assets/cov19_icon.png')
        .then((onValue) {
      myIcon = onValue;
    });
    markers = get_markers();

    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('    COVID-19\n     anonymus database of virus prsence', textAlign: TextAlign.center),
      ),
      body: Stack(
          children: [Container(
            height: MediaQuery.of(context).size.height,
            width: MediaQuery.of(context).size.width,
            child: GoogleMap(
              initialCameraPosition:
              CameraPosition(target: LatLng(50.049, 19.944), zoom: 14.0),
              markers: markers,
              onMapCreated: mapCreated,
            ),
          ),
            Align(
              alignment: Alignment.bottomCenter,
              child: Container(
                height: 100,
                width: MediaQuery.of(context).size.width,
                child: Column(
                  children: <Widget>[
                    Slider(
                      min: 1,
                      max: 30,
                      value: day,
                      onChanged: (value) {
                        setState(() {
                          day = value;
                        });
                      },
                      onChangeEnd: changeDay(day),
                    ),
                    Slider(
                      min: 1,
                      max: 24,
                      value: hour,
                      label: '$hour',
                      onChanged: (value) {
                        setState(() {
                          hour = value;
                        });
                      },
                      onChangeEnd: changeHour(hour),
                    ),
                  ],
                ),
              ),
            )
          ]
      ),
    );
  }

  //______________________________MARKERS_____________________________
  Set<Marker> get_markers() {
    markers.add(Marker(
        markerId: MarkerId('xxx'),
        draggable: false,
        icon: myIcon,
        position: LatLng(50.049, 19.944)
    ));
    return markers;
  }

  Set<Marker> getMarkers(data) {
    Set<Marker> newMarkers = Set();
    for(Virus single_marker in data) {
      newMarkers.add(Marker(markerId: MarkerId(newMarkers.length.toString()),
          draggable: false,
          icon: myIcon,
          position: LatLng(single_marker.lat, single_marker.long)));
    }
    return newMarkers;
  }

  void mapCreated(controller) {
    setState(() {
      _controller = controller;
    });
  }

  changeMarkers(var fetched_data){
    setState(() {
      markers = getMarkers(fetched_data);
    });
  }

  changeDay(var new_day) {
    fetchVirus(url).then((value){
      changeMarkers(value);
    });
  }

  changeHour(var new_hour) {
    fetchVirus(url).then((value) {
      changeMarkers(value);
    });
  }
}

//_________________________CONNECTION____________________________

class Virus {
  double long;
  double lat;

  Virus(this.long, this.lat);

  factory Virus.fromJson(Map<String, dynamic> json) {
    return Virus(double.parse(json['long']) as double, double.parse(json['lat']) as double);
  }}

List<Virus> parseVirus(String responseBody) {
  final parsed = json.decode(responseBody).cast<Map<String, dynamic>>();
  return parsed.map<Virus>((json) => Virus.fromJson(json)).toList();
}

Future<List<Virus>> fetchVirus(url) async {
  final response = await http.get(url);
  if (response.statusCode == 200) {
    return parseVirus(response.body);
  } else {
    throw Exception('Failed to load virus');
  }
}
