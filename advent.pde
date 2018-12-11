// advent
//
// Animate the opening of doors on an Advent Calendar and save frames
// of the animation to be combined into movies/GIFs
//
// Copyright (c) 2018 John Graham-Cumming

// day is the current day being opened during animation. Starts
// at 0 so that all the doors are drawn closed once.
int day = 0;

// Format of the Advent Calendar (rows x columms)
int h = 4;
int w = 6;

// The Advent Calendar to animate                
int [][] cal = {{ 9,  4, 18, 10, 15, 20},
                {16, 21, 12,  1, 22,  7},
                { 2,  6, 24,  5, 17, 13},
                {14,  8, 19, 11, 23,  3}};                
  
// The canvas size. Note that if you change this, change the size()
// function call in setup()
int cw = 640;
int ch = 480;

// filename for the frames output from the animation
String filename = "advent-";

// Door class represents a single Door is shown on the canvas
public class Door {  
  // (cx, cy) is the centre of the circle
  public int cx;
  public int cy;
  
  // d is the calculated door diameter
  private int d;
  
  // Entry in the calendar array
  private int calx;
  private int caly;

  Door(int x, int y) {
    // g is a gutter around the edge of the canvas where we won't draw doors
    // hdiam and vdiam are the maximum horizontal and vertical sizes for ellipses
    // one per door.
  
    int g = 16;
    int hdiam = (cw-g*2)/w;
    int vdiam = (ch-g*2)/h;
  
    // touch is the maximum size of a circle where they will touch
  
    int touch = (hdiam<vdiam)?hdiam:vdiam;
    d = touch * 80 / 100;
 
    cx = x * hdiam + g + hdiam/2;
    cy = y * vdiam + g + vdiam/2; 
    
    calx = x;
    caly = y;
  }
  
  // paint draws the door on the canvas
  
  void paint() {

    // If the door has been opened then color is grey, otherwise
    // alternative red and green for a Christmassy effect
  
    if (cal[caly][calx] < 0) {
      stroke(color(128,128,128));
      strokeWeight(4);
    } else {
      strokeWeight(2);
      if ((calx+caly)%2 == 0) {
        stroke(color(255,0,0));
      } else {
        stroke(color(0,255,0));
      }
    }
  
    noFill(); 
    textAlign(CENTER, CENTER);
    textSize(24);
    ellipse(cx, cy, d, d);
  
    fill(0);
    text(abs(cal[caly][calx]), cx, cy);
  }
  
  // arrow draws an arrow between a door and this door
  
  void arrow(Door src) {
    stroke(color(128,128,128));
    strokeWeight(4);
    line(src.cx, src.cy, cx, cy);
  }
}

Door [][] doors;

void clear() {
  background(255);
}

void setup() {
  size(640, 480);
  clear();
  
  // Initialize the doors with one Door per cal element
  // and generate a unique filename format for this
  // calendar
  
  doors = new Door[h][w];
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      doors[y][x] = new Door(x, y);
      filename += nf(cal[y][x]);
      filename += "-";
    }
  }
  
  filename += "####.png";
}

// Stores the (x, y) of the last door that was opened
int lx = -1;
int ly = -1;

void draw() {
  clear();
  
  for (int x = 0; x < w; x++) {
    for (int y = 0; y < h; y++) {
      if (cal[y][x] == day) {
        cal[y][x] = -day;
        
        if (day > 1) {
          doors[y][x].arrow(doors[ly][lx]);
        }
        
        lx = x;
        ly = y;
      }
      
      doors[y][x].paint();
    }
  }
  
  if (day <= 24) {
    saveFrame(filename);
    day += 1;
  }
}

  
  
