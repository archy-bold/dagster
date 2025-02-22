// Generated GraphQL types, do not edit manually.

import * as Types from '../../../graphql/types';

export type BackfillStatusesByAssetQueryVariables = Types.Exact<{
  backfillId: Types.Scalars['String'];
}>;

export type BackfillStatusesByAssetQuery = {
  __typename: 'Query';
  partitionBackfillOrError:
    | {__typename: 'BackfillNotFoundError'; message: string}
    | {
        __typename: 'PartitionBackfill';
        id: string;
        status: Types.BulkActionStatus;
        timestamp: number;
        endTimestamp: number | null;
        numPartitions: number | null;
        hasCancelPermission: boolean;
        hasResumePermission: boolean;
        isAssetBackfill: boolean;
        numCancelable: number;
        partitionNames: Array<string> | null;
        error: {
          __typename: 'PythonError';
          message: string;
          stack: Array<string>;
          errorChain: Array<{
            __typename: 'ErrorChainLink';
            isExplicitLink: boolean;
            error: {__typename: 'PythonError'; message: string; stack: Array<string>};
          }>;
        } | null;
        partitionStatusCounts: Array<{
          __typename: 'PartitionStatusCounts';
          runStatus: Types.RunStatus;
          count: number;
        }>;
        assetBackfillData: {
          __typename: 'AssetBackfillData';
          rootAssetTargetedPartitions: Array<string> | null;
          rootAssetTargetedRanges: Array<{
            __typename: 'PartitionKeyRange';
            start: string;
            end: string;
          }> | null;
          assetBackfillStatuses: Array<
            | {
                __typename: 'AssetPartitionsStatusCounts';
                numPartitionsTargeted: number;
                numPartitionsInProgress: number;
                numPartitionsMaterialized: number;
                numPartitionsFailed: number;
                assetKey: {__typename: 'AssetKey'; path: Array<string>};
              }
            | {
                __typename: 'UnpartitionedAssetStatus';
                inProgress: boolean;
                materialized: boolean;
                failed: boolean;
                assetKey: {__typename: 'AssetKey'; path: Array<string>};
              }
          >;
        } | null;
        partitionSet: {
          __typename: 'PartitionSet';
          name: string;
          pipelineName: string;
          repositoryOrigin: {
            __typename: 'RepositoryOrigin';
            repositoryName: string;
            repositoryLocationName: string;
          };
        } | null;
      }
    | {
        __typename: 'PythonError';
        message: string;
        stack: Array<string>;
        errorChain: Array<{
          __typename: 'ErrorChainLink';
          isExplicitLink: boolean;
          error: {__typename: 'PythonError'; message: string; stack: Array<string>};
        }>;
      };
};

export type PartitionBackfillFragment = {
  __typename: 'PartitionBackfill';
  id: string;
  status: Types.BulkActionStatus;
  timestamp: number;
  endTimestamp: number | null;
  numPartitions: number | null;
  hasCancelPermission: boolean;
  hasResumePermission: boolean;
  isAssetBackfill: boolean;
  numCancelable: number;
  partitionNames: Array<string> | null;
  error: {
    __typename: 'PythonError';
    message: string;
    stack: Array<string>;
    errorChain: Array<{
      __typename: 'ErrorChainLink';
      isExplicitLink: boolean;
      error: {__typename: 'PythonError'; message: string; stack: Array<string>};
    }>;
  } | null;
  partitionStatusCounts: Array<{
    __typename: 'PartitionStatusCounts';
    runStatus: Types.RunStatus;
    count: number;
  }>;
  assetBackfillData: {
    __typename: 'AssetBackfillData';
    rootAssetTargetedPartitions: Array<string> | null;
    rootAssetTargetedRanges: Array<{
      __typename: 'PartitionKeyRange';
      start: string;
      end: string;
    }> | null;
    assetBackfillStatuses: Array<
      | {
          __typename: 'AssetPartitionsStatusCounts';
          numPartitionsTargeted: number;
          numPartitionsInProgress: number;
          numPartitionsMaterialized: number;
          numPartitionsFailed: number;
          assetKey: {__typename: 'AssetKey'; path: Array<string>};
        }
      | {
          __typename: 'UnpartitionedAssetStatus';
          inProgress: boolean;
          materialized: boolean;
          failed: boolean;
          assetKey: {__typename: 'AssetKey'; path: Array<string>};
        }
    >;
  } | null;
  partitionSet: {
    __typename: 'PartitionSet';
    name: string;
    pipelineName: string;
    repositoryOrigin: {
      __typename: 'RepositoryOrigin';
      repositoryName: string;
      repositoryLocationName: string;
    };
  } | null;
};
