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
// Package app manages the main game loop.

package main

import (
	"fmt"
	_ "image/png"
	"log"
	"reflect"
	"runtime"

	"github.com/go-gl/gl/v4.1-core/gl"
	"github.com/go-gl/glfw/v3.1/glfw"
	"github.com/go-gl/mathgl/mgl32"
	"github.com/hurricanerix/shade/camera"
	"github.com/hurricanerix/shade/display"
	"github.com/hurricanerix/shade/entity"
	"github.com/hurricanerix/shade/events"
	"github.com/hurricanerix/shade/examples/03-basic-collisions/ball"
	"github.com/hurricanerix/shade/examples/03-basic-collisions/block"
	"github.com/hurricanerix/shade/examples/03-basic-collisions/player"
	"github.com/hurricanerix/shade/fonts"
	"github.com/hurricanerix/shade/shapes"
	"github.com/hurricanerix/shade/sprite"
	"github.com/hurricanerix/shade/time/clock"
)

const windowWidth = 640
const windowHeight = 480

func init() {
	// GLFW event handling must run on the main OS thread
	runtime.LockOSThread()
}

func main() {
	screen, err := display.SetMode("03-collisions", windowWidth, windowHeight)
	if err != nil {
		log.Fatalln("failed to set display mode:", err)
	}

	cam, err := camera.New()
	if err != nil {
		panic(err)
	}
	cam.Bind(screen.Program)

	font, err := fonts.SimpleASCII()
	if err != nil {
		panic(err)
	}
	font.Bind(screen.Program)

	clock, err := clock.New()
	if err != nil {
		panic(err)
	}

	objects := []entity.Collider{}

	blockSprite, err := loadSprite("assets/block32x32.png", "", 2, 1)
	if err != nil {
		panic(err)
	}
	blockSprite.Bind(screen.Program)
	objects = append(objects, block.New(0, float32(windowWidth)/4, float32(windowHeight)/2, blockSprite))

	ballSprite, err := loadSprite("assets/ball.png", "", 1, 1)
	if err != nil {
		panic(err)
	}
	ballSprite.Bind(screen.Program)
	objects = append(objects, ball.New(float32(windowWidth)/2, float32(windowHeight)/2, ballSprite))

	//shapes.NewCircle(mgl32.Vec2{float32(s.Width) / 2, float32(s.Height) / 2}, float32(s.Width)/2),
	tmpSprites := []*sprite.Context{blockSprite, ballSprite}
	tmpShapes := []*shapes.Shape{
		shapes.NewRect(0, float32(blockSprite.Width), 0, float32(blockSprite.Height)),
		shapes.NewCircle(mgl32.Vec2{float32(ballSprite.Width) / 2, float32(ballSprite.Height) / 2}, float32(ballSprite.Width)/2),
	}
	pl, err := player.New(0, 0, tmpSprites, tmpShapes, nil)
	if err != nil {
		panic(err)
	}
	efx := sprite.Effects{
		Scale: mgl32.Vec3{2.0, 2.0, 1.0},
	}

	var msg string
	//	sprites.Bind(screen.Program)
	for running := true; running; {
		dt := clock.Tick(30)

		screen.Fill(0.3, 0.3, 0.6)

		// TODO move this somewhere else (maybe a Clear method of display
		gl.Clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT)

		// TODO refector events to be cleaner
		if screen.Window.ShouldClose() {
			running = !screen.Window.ShouldClose()
		}

		for _, event := range events.Get() {
			if event.Action == glfw.Press && event.Key == glfw.KeyEscape {
				running = false
				event.Window.SetShouldClose(true)
			}

			if (event.Action == glfw.Press || event.Action == glfw.Repeat) && event.Key == glfw.KeySpace {
				pl.NextShape()
			}
			if !event.KeyEvent {
				pl.SetPos(&mgl32.Vec3{event.X, float32(windowHeight) - event.Y, 1.0})
			}
		}

		for _, e := range objects {
			d, ok := e.(entity.Entity)
			if ok {
				d.Draw()

				// TODO: Maybe compare the types rather than converted strings
				if reflect.TypeOf(d).String() == "*block.Block" {
					tmp := e.(*block.Block)
					pos := tmp.Pos()
					msg = fmt.Sprintf("Pos: (%.0f,%.0f)\n", pos[0], pos[1])
					msg += fmt.Sprintf("Data: [\n")
					msg += fmt.Sprintf("  Left: %.0f\n", tmp.Shape.Data[0])
					msg += fmt.Sprintf("  Right: %.0f\n", tmp.Shape.Data[1])
					msg += fmt.Sprintf("  Top: %.0f\n", tmp.Shape.Data[2])
					msg += fmt.Sprintf("  Bottom: %.0f\n", tmp.Shape.Data[3])
					msg += fmt.Sprintf("]\n")
					//_, h := font.SizeText(&efx, msg)
					font.DrawText(mgl32.Vec3{0, float32(windowHeight) - 16, 0}, &efx, msg)
				} else {
					tmp := e.(*ball.Ball)
					pos := tmp.Pos()
					msg = fmt.Sprintf("Pos: (%.0f,%.0f)\n", pos[0], pos[1])
					msg += fmt.Sprintf("Data: [\n")
					msg += fmt.Sprintf("  Center: (%.0f, %.0f)\n", tmp.Shape.Data[0], tmp.Shape.Data[1])
					msg += fmt.Sprintf("  Radius: %.0f\n", tmp.Shape.Data[2])
					msg += fmt.Sprintf("]\n")
					w, _ := font.SizeText(&efx, msg)
					font.DrawText(mgl32.Vec3{float32(windowWidth) - w, float32(windowHeight) - 16, 0}, &efx, msg)
				}
			}

		}

		pl.Update(dt/1000.0, objects)
		pl.Draw()

		pos := pl.Pos()
		msg = fmt.Sprintf("(%.0f,%.0f)\n", pos[0], pos[1])
		if pl.Collision == nil {
			msg += fmt.Sprintf("Collision: nil\n")
		} else {
			c, ok := pl.Collision.Hit.(entity.Entity)
			if ok {
				msg += fmt.Sprintf("Collision: {\n")
				msg += fmt.Sprintf("  Type: %T\n", c)
				msg += fmt.Sprintf("  Dir: (%.1f,%.1f,%.1f)\n", pl.Collision.Dir[0], pl.Collision.Dir[1], pl.Collision.Dir[2])
				msg += fmt.Sprintf("}\n")
			}
		}
		b := pl.Bounds()

		if b.Type == "rect" {
			msg += fmt.Sprintf("Data: [\n")
			msg += fmt.Sprintf("  Left: %.0f\n", b.Data[0])
			msg += fmt.Sprintf("  Right: %.0f\n", b.Data[1])
			msg += fmt.Sprintf("  Top: %.0f\n", b.Data[2])
			msg += fmt.Sprintf("  Bottom: %.0f\n", b.Data[3])
			msg += fmt.Sprintf("]\n")
		} else {
			msg += fmt.Sprintf("Data: [\n")
			msg += fmt.Sprintf("  Center: (%.0f, %.0f)\n", b.Data[0], b.Data[1])
			msg += fmt.Sprintf("  Radius: %.0f\n", b.Data[2])
			msg += fmt.Sprintf("]\n")
		}
		pos = pl.Pos()
		font.DrawText(mgl32.Vec3{pos[0], pos[1] - 16, 0}, &efx, msg)

		screen.Flip()

		// TODO refector events to be cleaner
		glfw.PollEvents()
	}
}

func loadSprite(colorName, normalName string, framesWide, framesHigh int) (*sprite.Context, error) {
	c, err := sprite.LoadAsset(colorName)
	if err != nil {
		return nil, err
	}

	n, err := sprite.LoadAsset(normalName)
	if err != nil {
		return nil, err
	}

	s, err := sprite.New(c, n, framesWide, framesHigh)
	if err != nil {
		return nil, err
	}

	return s, nil
}