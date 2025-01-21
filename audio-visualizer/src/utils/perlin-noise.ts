import * as THREE from "three";

var SimplexNoise: any = function (this: any, r?: any) {
	if (r == undefined) r = Math;
	this.grad3 = [
		[1, 1, 0],
		[-1, 1, 0],
		[1, -1, 0],
		[-1, -1, 0],
		[1, 0, 1],
		[-1, 0, 1],
		[1, 0, -1],
		[-1, 0, -1],
		[0, 1, 1],
		[0, -1, 1],
		[0, 1, -1],
		[0, -1, -1],
	];
	this.p = [];
	for (var i = 0; i < 256; i++) {
		this.p[i] = Math.floor(r.random() * 256);
	}
	// To remove the need for index wrapping, double the permutation table length
	this.perm = [];
	for (var i = 0; i < 512; i++) {
		this.perm[i] = this.p[i & 255];
	}

	// A lookup table to traverse the simplex around a given point in 4D.
	// Details can be found where this table is used, in the 4D noise method.
	this.simplex = [
		[0, 1, 2, 3],
		[0, 1, 3, 2],
		[0, 0, 0, 0],
		[0, 2, 3, 1],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[1, 2, 3, 0],
		[0, 2, 1, 3],
		[0, 0, 0, 0],
		[0, 3, 1, 2],
		[0, 3, 2, 1],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[1, 3, 2, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[1, 2, 0, 3],
		[0, 0, 0, 0],
		[1, 3, 0, 2],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[2, 3, 0, 1],
		[2, 3, 1, 0],
		[1, 0, 2, 3],
		[1, 0, 3, 2],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[2, 0, 3, 1],
		[0, 0, 0, 0],
		[2, 1, 3, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[2, 0, 1, 3],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[3, 0, 1, 2],
		[3, 0, 2, 1],
		[0, 0, 0, 0],
		[3, 1, 2, 0],
		[2, 1, 0, 3],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[3, 1, 0, 2],
		[0, 0, 0, 0],
		[3, 2, 0, 1],
		[3, 2, 1, 0],
	];
};

SimplexNoise.prototype.dot = function (g: any, x: any, y: any) {
	return g[0] * x + g[1] * y;
};

SimplexNoise.prototype.noise = function (xin: any, yin: any) {
	var n0, n1, n2; // Noise contributions from the three corners
	// Skew the input space to determine which simplex cell we're in
	var F2 = 0.5 * (Math.sqrt(3.0) - 1.0);
	var s = (xin + yin) * F2; // Hairy factor for 2D
	var i = Math.floor(xin + s);
	var j = Math.floor(yin + s);
	var G2 = (3.0 - Math.sqrt(3.0)) / 6.0;
	var t = (i + j) * G2;
	var X0 = i - t; // Unskew the cell origin back to (x,y) space
	var Y0 = j - t;
	var x0 = xin - X0; // The x,y distances from the cell origin
	var y0 = yin - Y0;
	// For the 2D case, the simplex shape is an equilateral triangle.
	// Determine which simplex we are in.
	var i1, j1; // Offsets for second (middle) corner of simplex in (i,j) coords
	if (x0 > y0) {
		i1 = 1;
		j1 = 0;
	} // lower triangle, XY order: (0,0)->(1,0)->(1,1)
	else {
		i1 = 0;
		j1 = 1;
	} // upper triangle, YX order: (0,0)->(0,1)->(1,1)
	// A step of (1,0) in (i,j) means a step of (1-c,-c) in (x,y), and
	// a step of (0,1) in (i,j) means a step of (-c,1-c) in (x,y), where
	// c = (3-sqrt(3))/6
	var x1 = x0 - i1 + G2; // Offsets for middle corner in (x,y) unskewed coords
	var y1 = y0 - j1 + G2;
	var x2 = x0 - 1.0 + 2.0 * G2; // Offsets for last corner in (x,y) unskewed coords
	var y2 = y0 - 1.0 + 2.0 * G2;
	// Work out the hashed gradient indices of the three simplex corners
	var ii = i & 255;
	var jj = j & 255;
	var gi0 = this.perm[ii + this.perm[jj]] % 12;
	var gi1 = this.perm[ii + i1 + this.perm[jj + j1]] % 12;
	var gi2 = this.perm[ii + 1 + this.perm[jj + 1]] % 12;
	// Calculate the contribution from the three corners
	var t0 = 0.5 - x0 * x0 - y0 * y0;
	if (t0 < 0) n0 = 0.0;
	else {
		t0 *= t0;
		n0 = t0 * t0 * this.dot(this.grad3[gi0], x0, y0); // (x,y) of grad3 used for 2D gradient
	}
	var t1 = 0.5 - x1 * x1 - y1 * y1;
	if (t1 < 0) n1 = 0.0;
	else {
		t1 *= t1;
		n1 = t1 * t1 * this.dot(this.grad3[gi1], x1, y1);
	}
	var t2 = 0.5 - x2 * x2 - y2 * y2;
	if (t2 < 0) n2 = 0.0;
	else {
		t2 *= t2;
		n2 = t2 * t2 * this.dot(this.grad3[gi2], x2, y2);
	}
	// Add contributions from each corner to get the final noise value.
	// The result is scaled to return values in the interval [-1,1].
	return 70.0 * (n0 + n1 + n2);
};

export default function apply_perlin_noise(
	positions: THREE.TypedArray,
	min_length: number,
	max_length: number,
	scale?: number,
	smoothing?: number,
	damping?: number
) {
	scale = scale || 1;
	smoothing = smoothing || 1.0;
	damping = damping || 0.125;

	let simplex = new SimplexNoise();

	for (let i = 0; i < positions.length; i += 3) {
		let noise =
			simplex.noise(
				positions[i] / smoothing,
				positions[i + 1] / smoothing
			) * scale;

		let a = positions[i];
		let b = positions[i + 1];
		let theta = Math.atan2(b, a);

		let r = Math.sqrt(a * a + b * b);

		let new_length = Math.min(Math.max(min_length, r + noise), max_length);

		const position_vec3 = new THREE.Vector3(
			positions[i],
			positions[i + 1],
			1
		);

		const targetPosition = new THREE.Vector3(
			new_length * Math.cos(theta),
			new_length * Math.sin(theta),
			1
		);

		const newPosition = position_vec3.lerp(targetPosition, damping);

		positions[i] = newPosition.x;
		positions[i + 1] = newPosition.y;
	}

	return positions;
}
