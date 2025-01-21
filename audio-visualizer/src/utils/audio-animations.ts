import * as THREE from "three";

export default function apply_basic_circle_effect(
	positions: THREE.TypedArray,
	magnitude: number,
	min_length: number,
	max_length: number,
	damping: number = 0.0625
) {
	for (let i = 0; i < positions.length; i += 3) {
		let a = positions[i];
		let b = positions[i + 1];
		let theta = Math.atan2(b, a);

		let randomMagnitude = Math.random() * 50 + magnitude;

		let r = Math.sqrt(a * a + b * b);

		let new_length = Math.min(
			Math.max(min_length, randomMagnitude),
			max_length
		);

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
