// Copyright 2016 Richard Hawkins
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package sprite

import "github.com/hurricanerix/shade/entity"

// Collide TODO doc
func Collide(t entity.Entity, g *[]entity.Entity, dokill bool) []Sprite {
	/*
		var hits []Sprite
		if g == nil {
			return nil
		}
		for ttb := range t.Bounds() {
			for _, s := range g.Sprites {
				for stb := range s.Bounds() {
					if testBounds(ttb, stb) {
						hits = append(hits, s)
					}
				}
			}
		}
		return hits
	*/
	return nil
}
