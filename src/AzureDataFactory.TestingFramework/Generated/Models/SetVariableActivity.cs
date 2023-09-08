// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.

// <auto-generated/>

#nullable disable

using Azure.Core;
using Azure.Core.Expressions.DataFactory;

namespace AzureDataFactory.TestingFramework.Models
{
    /// <summary> Set value for a Variable. </summary>
    public partial class SetVariableActivity : ControlActivity
    {
        /// <summary> Initializes a new instance of SetVariableActivity. </summary>
        /// <param name="name"> Activity name. </param>
        /// <exception cref="ArgumentNullException"> <paramref name="name"/> is null. </exception>
        public SetVariableActivity(string name) : base(name)
        {
            Argument.AssertNotNull(name, nameof(name));

            ActivityType = "SetVariable";
        }

        /// <summary> Initializes a new instance of SetVariableActivity. </summary>
        /// <param name="name"> Activity name. </param>
        /// <param name="activityType"> Type of activity. </param>
        /// <param name="description"> Activity description. </param>
        /// <param name="state"> Activity state. This is an optional property and if not provided, the state will be Active by default. </param>
        /// <param name="onInactiveMarkAs"> Status result of the activity when the state is set to Inactive. This is an optional property and if not provided when the activity is inactive, the status will be Succeeded by default. </param>
        /// <param name="dependsOn"> Activity depends on condition. </param>
        /// <param name="userProperties"> Activity user properties. </param>
        /// <param name="additionalProperties"> Additional Properties. </param>
        /// <param name="policy"> Activity policy. </param>
        /// <param name="variableName"> Name of the variable whose value needs to be set. </param>
        /// <param name="value"> Value to be set. Could be a static value or Expression. </param>
        /// <param name="setSystemVariable"> If set to true, it sets the pipeline run return value. </param>
        internal SetVariableActivity(string name, string activityType, string description, PipelineActivityState? state, ActivityOnInactiveMarkAs? onInactiveMarkAs, IList<PipelineActivityDependency> dependsOn, IList<PipelineActivityUserProperty> userProperties, IDictionary<string, DataFactoryElement<string>> additionalProperties, SecureInputOutputPolicy policy, string variableName, DataFactoryElement<string> value, Dictionary<string, DataFactoryElement<string>> pipelineReturnValues, bool? setSystemVariable) : base(name, activityType, description, state, onInactiveMarkAs, dependsOn, userProperties, additionalProperties)
        {
            Policy = policy;
            VariableName = variableName;
            Value = value;
            PipelineReturnValues = pipelineReturnValues;
            SetSystemVariable = setSystemVariable;
            ActivityType = activityType ?? "SetVariable";
        }

        /// <summary> Activity policy. </summary>
        public SecureInputOutputPolicy Policy { get; set; }
        /// <summary> Name of the variable whose value needs to be set. </summary>
        public string VariableName { get; set; }
        /// <summary> Value to be set. Could be a static value or Expression. </summary>
        public DataFactoryElement<string> Value { get; set; }
        /// <summary> Value to be set. Could be a static value or Expression. </summary>
        public Dictionary<string, DataFactoryElement<string>> PipelineReturnValues { get; set; }
        /// <summary> If set to true, it sets the pipeline run return value. </summary>
        public bool? SetSystemVariable { get; set; }
    }
}
