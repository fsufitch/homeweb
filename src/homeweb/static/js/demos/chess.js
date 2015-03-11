var count = 0;

function get_board_array() {
    var rows = [8, 7, 6, 5, 4, 3, 2, 1];            // Top to bottom
    var cols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']; // Left to right
    var boardarr = [];
    for (var r=0; r<rows.length; r++) {
	var row = [];
	for (var c=0; c<cols.length; c++) {
	    var cell = {
		'text': cols[c] + rows[r],
		'is_black': (c+r)%2==0,
	    };
	    row.push(cell);
	}
	boardarr.push(row);
    }
    return boardarr;
}

function draw_stuff() {
    var board = document.getElementById("chessboard");
    var ctx = board.getContext("2d");
    ctx.fillStyle = "#FF0000";

    coord_start = count*10;
    coord_end = count*10+10;
    ctx.fillRect(coord_start,coord_start,coord_end,coord_end);

    count += 1;
}

function draw_board() {
    var board = document.getElementById("chessboard");
    var ctx = board.getContext("2d");
    
    var boardarr = get_board_array();
    var squarecount = 0;
    for (var r=0; r<boardarr.length; r++) {
	var row = boardarr[r];
	for (var c=0; c<row.length; c++) {
	    var cell = row[c];
	    ctx.fillStyle = cell['is_black'] ? "#444" : "#FFF";
	    var x = c*100;
	    var y = r*100;
	    ctx.fillRect(x, y, x+100, y+100);
	    ctx.font = "30px Serif";
	    ctx.strokeText(squarecount+": "+cell['text'], x, y+50);
	    squarecount += 1;
	    console.log(x+" "+y+" "+cell);
	}
    }
}

function setup() {
    $("#drawagain").click(draw_stuff);
    draw_board();
}

$(document).ready(setup);
