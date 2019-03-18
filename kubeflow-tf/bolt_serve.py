# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import kfp.dsl as dsl

@dsl.pipeline(
  name='Bolt Classification',
  description='END to END kubeflow demo with TensorRT Inference Server'
)
def bolt( #pylint: disable=unused-argument
    trtserver_name: dsl.PipelineParam = dsl.PipelineParam(name='trtserver_name', value='trtserver'),
    model_name: dsl.PipelineParam = dsl.PipelineParam(name='model_name', value='bolt'),
    model_version: dsl.PipelineParam = dsl.PipelineParam(name='model_version', value='1'),
    webapp_prefix: dsl.PipelineParam = dsl.PipelineParam(name='webapp_prefix', value = 'webapp'),
    webapp_port: dsl.PipelineParam = dsl.PipelineParam(name='webapp_port', value='80') ):

  serve = dsl.ContainerOp(
      name='serve',
      image='gcr.io/gtc-2019-demo/ml-pipeline-kubeflow-trtisserve',
      arguments=["--trtserver_name", trtserver_name,
          "--model_path", 'gs://test-gtc-demo-2019/example_saved_model'
          ]
      )

  webapp = dsl.ContainerOp(
      name='webapp',
      image='gcr.io/gtc-2019-demo/ml-pipeline-trtis-webapp-launcher',
      arguments=["--workflow_name", '%s' % ('{{workflow.name}}',),
                 "--trtserver_name", trtserver_name,
                 "--model_name", model_name,
                 "--model_version", str(model_version),
                 "--webapp_prefix", webapp_prefix,
                 "--webapp_port", str(webapp_port)
                 ]
      )


if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(bolt, __file__ + '.tar.gz')
