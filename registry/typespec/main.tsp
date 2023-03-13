import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

@service({
    title: "xregistry",
    description: "First pass of the xregistry api",
    version: "0.0.1",
    termsOfService: "https://github.com/cloudevents/",
    contact: {
      name: "Mark Weitzel et al.",
      url: "https://github.com/cloudevents/spec/blob/main/registry/spec.md"
    }
  })
@server("https://xregistry.example/", "Actual server to be set during client setup")
@route("/")
namespace xregistry;

@error
@doc("Error response")
model Error {
    @doc("A server-defined code that uniquely identifies the error.")
    code: string;
    @doc("Top-level error object")
    error: ErrorDetail;
}

@doc("Error details")
model ErrorDetail {
  @doc("A server-defined code that uniquely identifies the error.")
  code: string;
  @doc("A human-readable representation of the error.")
  message: string;
  @doc("An array of details about specific errors that led to this reported error.")
  details?: ErrorDetail[];
}

model Patch<T> {
  @header contentType: "application/merge-patch+json";
  ...T;
}

model List<T> {
  @doc("List of elements")
  value: T[];
  @doc("A link to the next page of results if present.")
  nextLink?: url;
}

model RegistryTag {
    key: string;
    value: string;
}

model CommonMetadata {
    singlular: string;
    plural: string;
    schema?: url;
    resources?:[CommonMetadata]
}

model RegistryMetadata {
    registryMetadata:{
      name: string;
      description: string;
      tags: RegistryTag[];
      groups:[CommonMetadata];
    }
}



model RegistryResource {
    @doc("A unique identifier of the entity.")
    @path
    id: string;

    @doc("A human readable name of the entity. Note that implementations MAY choose to enforce constraints on this value. For example, they could mandate that id and name be the same value. How any such requirement is shared with all parties is out of scope of this specification.")
    name?: string;
    
    @doc("A human readable summary of the purpose of the entity.")
    description?: string;
    
    @doc("A mechanism in which additional metadata about the entity can be stored without changing the schema of the entity.")
    tags?: RegistryTag[];

    @doc("A numeric value representing a specific instance of an entity. Note that versions of an entity can be modified without changing the version value. Often this value, or when a new version is created, is controlled by a user of the Registry.")
    version?: int32;

    @doc("A numeric value used to determine whether an entity has been modified. Each time the associated entity is updated, this value MUST be set to a new value that is greater than the current one. Note that unlike version, this attribute is most often managed by the Registry itself. Additionally, if an entity is created that is based on another entity (e.g. a new version of an entity is created), then the new entity's `epoch` value can be reset (e.g. to zero) since the scope of its values is the entity.")
    epoch?: int64;

    @doc("A unique URL for the entity. The URL MUST be a combination of the base URL for the list of resources of this type of entity appended with the id of the entity.")
    self?: url;

    @doc("A reference to the user or component that was responsible for the creation of this entity. This specification makes no requirement on the semantics or syntax of this value.")
    createdBy?: string;

    @doc("The date/time of when the entity was created.")
    createdOn?: zonedDateTime;

    @doc("A reference to the user or component that was responsible for the the latest update of this entity. This specification makes no requirement on the semantics or syntax of this value")
    modifiedBy?: string;

    @doc("The date/time of when the entity was last updated.")
    modifiedOn?: zonedDateTime;
    
    @doc("A URI-Reference to additional documentation about this entity. This specification does not place any constraints on the data returned from an HTTP GET to this value.")
    docs?: string;
}

// model a group of resources
model Group {
 @path 
 id:string;
 resources: RegistryResource[];
}

// Interfaces 
interface RegistryItemsInterface<T, P = {}> {
  @get list(...P): List<T> | Error;
  @get read(...P, @path id: string): T | Error;
  @put create(...P, @body body: T): T | Error;
  @patch update(...P, @body body: Patch<T>): T | Error;
  @delete delete(...P, @path id: string): void | Error;
}

@route("/groups")
@tag("Groups")
interface Groups extends RegistryItemsInterface<Group> {
}

//Define a "local" model here to make the interface more modular & resuable
model GroupPathId { @path groupId: string }

@route("groups/{groupId}/resources/")
@tag("Resources")
interface Resources extends RegistryItemsInterface<RegistryResource, GroupPathId> {
}

@route("/registryMetdata")
interface RegistryMetadataInterface {
  @get read(): RegistryMetadata | Error;
}