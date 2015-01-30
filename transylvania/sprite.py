# Copyright 2014 Richard Hawkins
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import ctypes
import json
import numpy
import os.path

import OpenGL.GL.shaders
from OpenGL.GL import (
    glActiveTexture, glAttachShader, glBindAttribLocation, glBindBuffer,
    glBindVertexArray,
    glBindTexture, glBufferData, glCreateProgram, glDrawArrays,
    glEnableVertexAttribArray, glGenBuffers, glGenTextures, glGenVertexArrays,
    glGetProgramInfoLog, glGetProgramiv,
    glGetUniformLocation, glLinkProgram,
    glTexImage2D,
    glTexParameteri,
    glUniform1i, glUniform1f, glUniform3fv, glUniformMatrix3fv,
    glUniformMatrix4fv,
    glUseProgram,
    glVertexAttribPointer)
from OpenGL.GL import (
    GL_ARRAY_BUFFER, GL_FLOAT,
    GL_FRAGMENT_SHADER, GL_LINEAR, GL_LINK_STATUS, GL_REPEAT, GL_RGBA,
    GL_TEXTURE0, GL_TEXTURE1, GL_TEXTURE_2D,
    GL_TEXTURE_BASE_LEVEL,
    GL_TEXTURE_MAG_FILTER, GL_TEXTURE_MAX_LEVEL, GL_TEXTURE_MIN_FILTER,
    GL_TEXTURE_WRAP_S, GL_TEXTURE_WRAP_T, GL_TRIANGLES, GL_TRUE,
    GL_STATIC_DRAW,
    GL_UNSIGNED_BYTE, GL_VERTEX_SHADER)
from PIL import Image

from transylvania.gmath import get_3x3_transform, get_4x4_transform


class Sprite(object):
    def update(*args):
        pass

    def add(*groups):
        pass

    def remove(*groups):
        pass

    def kill():
        pass

    def alive():
        pass

    def groups():
        pass


# vertices = [0.0, 0.0, 0.0, 1.0,
#             1.0, 0.0, 0.0, 1.0,
#             1.0, 1.0, 0.0, 1.0,
#             0.0, 1.0, 0.0, 1.0,
#             0.0, 0.0, 0.0, 1.0,
#             1.0, 1.0, 0.0, 1.0]
# vertices = numpy.array(vertices, dtype=numpy.float32)
#
# normals = [0.0, 0.0, 1.0,
#            0.0, 0.0, 1.0,
#            0.0, 0.0, 1.0,
#            0.0, 0.0, 1.0,
#            0.0, 0.0, 1.0,
#            0.0, 0.0, 1.0]
# normals = numpy.array(normals, dtype=numpy.float32)
#
# tangents = [1.0, 0.0, 0.0,
#             1.0, 0.0, 0.0,
#             1.0, 0.0, 0.0,
#             1.0, 0.0, 0.0,
#             1.0, 0.0, 0.0,
#             1.0, 0.0, 0.0]
# tangents = numpy.array(tangents, dtype=numpy.float32)
#
# tex_coords = [0.0, 1.0, 1.0,
#               1.0, 1.0, 1.0,
#               1.0, 0.0, 1.0,
#               0.0, 0.0, 1.0,
#               0.0, 1.0, 1.0,
#               1.0, 0.0, 1.0]
# tex_coords = numpy.array(tex_coords, dtype=numpy.float32)
#
# vao = None
# shader = None
# shader_locs = None
#
#
# def get_vao():
#     global vao
#     global shader_locs
#     if vao:
#         return vao
#     shader_locs = {'mc_vertex': 0, 'mc_normal': 1, 'mc_tangent': 2,
#                    'TexCoord0': 3}
#     vao = glGenVertexArrays(1)
#     glBindVertexArray(vao)
#
#     vertex_buffer = glGenBuffers(1)
#     glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
#     glVertexAttribPointer(shader_locs['mc_vertex'], 4, GL_FLOAT, False, 0,
#                           ctypes.c_void_p(0))
#     glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), vertices, GL_STATIC_DRAW)
#
#     normals_buf = glGenBuffers(1)
#     glBindBuffer(GL_ARRAY_BUFFER, normals_buf)
#     glVertexAttribPointer(shader_locs['mc_normal'], 3, GL_FLOAT, False, 0,
#                           ctypes.c_void_p(0))
#     glBufferData(GL_ARRAY_BUFFER, 4 * len(normals), normals,
#                  GL_STATIC_DRAW)
#
#     tangents_buf = glGenBuffers(1)
#     glBindBuffer(GL_ARRAY_BUFFER, tangents_buf)
#     glVertexAttribPointer(shader_locs['mc_tangent'], 3, GL_FLOAT, False, 0,
#                           ctypes.c_void_p(0))
#     glBufferData(GL_ARRAY_BUFFER, 4 * len(tangents), tangents,
#                  GL_STATIC_DRAW)
#
#     tex_coords_buf = glGenBuffers(1)
#     glBindBuffer(GL_ARRAY_BUFFER, tex_coords_buf)
#     glVertexAttribPointer(shader_locs['TexCoord0'], 3, GL_FLOAT, False, 0,
#                           ctypes.c_void_p(0))
#     glBufferData(GL_ARRAY_BUFFER, 4 * len(tex_coords), tex_coords,
#                  GL_STATIC_DRAW)
#
#     glBindBuffer(GL_ARRAY_BUFFER, 0)
#     glBindVertexArray(0)
#     return vao
#
#
# def get_shader():
#     global shader
#     global shader_locs
#     if shader:
#         return (shader, shader_locs)
#
#     shader_dir = os.path.realpath(__file__)
#     shader_dir = shader_dir.split('/')
#     shader_dir.pop()
#     shader_dir.append('shaders')
#     shader_dir = '/'.join(shader_dir)
#
#     vert_shader_src = open('{0}/sprite.vert'.format(shader_dir)).read()
#     frag_shader_src = open('{0}/sprite.frag'.format(shader_dir)).read()
#
#     vert_prog = OpenGL.GL.shaders.compileShader(
#         vert_shader_src, GL_VERTEX_SHADER)
#     frag_prog = OpenGL.GL.shaders.compileShader(
#         frag_shader_src, GL_FRAGMENT_SHADER)
#
#     shader = glCreateProgram()
#     glAttachShader(shader, vert_prog)
#     glAttachShader(shader, frag_prog)
#
#     for attrib in shader_locs:
#         glBindAttribLocation(shader, shader_locs[attrib], attrib)
#
#     glLinkProgram(shader)
#     if glGetProgramiv(shader, GL_LINK_STATUS) != GL_TRUE:
#         raise RuntimeError(glGetProgramInfoLog(shader))
#
#     for name in ['model_matrix', 'view_matrix', 'proj_matrix', 'tex_matrix',
#                  'ColorMap', 'NormalMap', 'light_position', 'light_color',
#                  'light_power']:
#         shader_locs[name] = glGetUniformLocation(shader, name)
#
#     return (shader, shader_locs)
#
#
# class SpriteBuilder(object):
#     """
#     Handles reading in sprite resources and creating a sprite from them.
#     """
#
#     @staticmethod
#     def build(path):
#         data_path = '{0}/data.json'.format(path)
#         if not os.path.isfile(data_path):
#             raise Exception('file {0} does not exist.'.format(data_path))
#         data = json.loads(open(data_path).read())
#
#         tex_data = {'color': None, 'normal': None}
#         color_path = '{0}/color.png'.format(path)
#         if not os.path.isfile(color_path):
#             raise Exception('file {0} does not exist.'.format(color_path))
#         img = Image.open(color_path)
#         width, height = img.size
#         tex_data['color'] = img.convert("RGBA").tostring("raw", "RGBA")
#
#         normal_path = '{0}/normal.png'.format(path)
#         if os.path.isfile(normal_path):
#             img = Image.open(normal_path)
#         else:
#             img = Image.new("RGBA", [width, height], (128, 128, 255, 255))
#         tex_data['normal'] = img.convert("RGBA").tostring("raw", "RGBA")
#
#         return Sprite(width, height, data, tex_data)
#
#
# class SpriteManager(object):
#     """
#     Manages sprites such that they can be used many times while only being
#     loaded once.
#     """
#
#     def __init__(self, sprite_dir):
#         """
#         @param sprite_dir:
#         @type sprite_dir: string
#         """
#         self.sprite_dir = sprite_dir
#         self.sprites = {}
#
#     def load(self, *names):
#         """
#         @param names:
#         @type names:
#         """
#         for name in names:
#             path = '{0}/{1}'.format(self.sprite_dir, name)
#             self.sprites[name] = SpriteBuilder.build(path)
#
#     def get_sprite(self, path):
#         """
#         @param path:
#         @type path:
#         @return:
#         @rtype:
#         """
#         return self.sprites[path]
#
#
# class Sprite(object):
#     """
#     Handles texturing images on a polygon.
#     """
#
#     def __init__(self, width, height, data, tex_data):
#         """
#         Initialize the OpenGL things needed to render the polygon.
#         @param data:
#         @type data:
#         @param tex_data:
#         @type tex_data:
#         """
#         self.width = width
#         self.height = height
#         self.data = data
#         self.tex_data = tex_data
#         self.texture_ids = None
#
#     def _bind_textures(self, data):
#         samplers = {
#             'color': GL_TEXTURE0,
#             'normal': GL_TEXTURE1}
#
#         for map_type in data:
#             if data[map_type] is None:
#                 continue
#             if self.texture_ids is None:
#                 self.texture_ids = {'color': None, 'normal': None}
#             if self.texture_ids[map_type] is not None:
#                 glActiveTexture(samplers[map_type])
#                 glBindTexture(GL_TEXTURE_2D, self.texture_ids[map_type])
#                 continue
#             self.texture_ids[map_type] = glGenTextures(1)
#             glActiveTexture(samplers[map_type])
#             glBindTexture(GL_TEXTURE_2D, self.texture_ids[map_type])
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#             glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#             glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0,
#                          GL_RGBA, GL_UNSIGNED_BYTE, data[map_type])
#
#     def draw(self, proj_matrix, view_matrix, x, y, layer=0,
#              frame_x=0, frame_y=0, lights=None):
#         """
#         Draw the sprite.
#
#         @param proj_mat: projection matrix to be passed to the shader.
#         @type proj_mat: 4x4 matrix
#         """
#         vao = get_vao()
#         (shader, shader_locs) = get_shader()
#         self._bind_textures(self.tex_data)
#
#         glBindVertexArray(vao)
#         glUseProgram(shader)
#
#         glEnableVertexAttribArray(shader_locs['mc_vertex'])
#         glEnableVertexAttribArray(shader_locs['mc_normal'])
#         glEnableVertexAttribArray(shader_locs['mc_tangent'])
#         glEnableVertexAttribArray(shader_locs['TexCoord0'])
#
#         model_matrix = get_4x4_transform(
#             scale_x=self.data['frame']['size']['width'],
#             scale_y=self.data['frame']['size']['height'],
#             trans_x=x, trans_y=y, trans_z=layer)
#         glUniformMatrix4fv(shader_locs['model_matrix'], 1, GL_TRUE,
#                            model_matrix)
#
#         glUniformMatrix4fv(shader_locs['view_matrix'], 1, GL_TRUE,
#                            view_matrix)
#
#         glUniformMatrix4fv(shader_locs['proj_matrix'], 1, GL_TRUE,
#                            proj_matrix)
#
#         scale_x = 1.0/self.data['frame']['count']['x']
#         scale_y = 1.0/self.data['frame']['count']['y']
#         trans_x = frame_x * scale_x
#         trans_y = frame_y * scale_y
#         tex_matrix = get_3x3_transform(scale_x, scale_y, trans_x, trans_y)
#         glUniformMatrix3fv(shader_locs['tex_matrix'], 1, GL_TRUE, tex_matrix)
#
#         if self.tex_data['color']:
#             glUniform1i(shader_locs['ColorMap'], 0)
#
#         if self.tex_data['normal']:
#             glUniform1i(shader_locs['NormalMap'], 1)
#
#         if lights:
#             glUniform3fv(shader_locs['light_position'], 1,
#                          lights[0].get_position())
#             glUniform3fv(shader_locs['light_color'], 1,
#                          lights[0].get_color())
#             glUniform1f(shader_locs['light_power'], lights[0].get_power())
#
#         glDrawArrays(GL_TRIANGLES, 0, int(len(vertices) / 4.0))
#
#         glBindVertexArray(0)
#         glUseProgram(0)
