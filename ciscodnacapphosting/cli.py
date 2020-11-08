import json
import ciscodnacapphosting
import click


@click.group(chain=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    pass

@cli.command("config")
@click.option("--hostname", required=True)
@click.option("--username", required=True)
@click.option("--password", required=True)
@click.option("--secure/--no-secure", default=True)
@click.option("--encode/--no-decode", default=False)
@click.pass_context
def dnac_config(ctx, hostname, username, password, secure, encode):
    if encode != None:
        status = ciscodnacapphosting.Api.config(
        hostname, username, password, secure, operation="encode"
    )
    else:
        status = ciscodnacapphosting.Api.config(
            hostname, username, password, secure, operation="write"
        )
    if status[0] is True:
        click.echo("Success: Config Updated")
    else:
        click.echo("Error: Config couldn't be updated")
    return


@cli.command("app")
@click.option("--id", required=False)
@click.option("--image", required=False)
@click.option("--tag", required=False)
@click.pass_context
def app(ctx, id, image, tag):
    dnac_app = ciscodnacapphosting.Api()
    if id != None:
        if tag != None:
            app = dnac_app.get(appId=id, tag=tag)
            click.echo(json.dumps(app, indent=4))
            return
        app = dnac_app.get(appId=id)
        click.echo(json.dumps(app, indent=4))
        return
    if image != None:
        if tag != None:
            app = dnac_app.get(image=image, tag=tag)
            click.echo(json.dumps(app, indent=4))
            return
        app = dnac_app.get(image=image)
        click.echo(json.dumps(app, indent=4))
        return
    apps = dnac_app.get()
    for app in apps["data"]:
        click.echo(json.dumps(app, indent=4))
    return


@cli.command("upload")
@click.option("--file", required=True)
@click.option("--categories", required=True)
@click.pass_context
def upload(ctx, file, categories):
    dnac_app = ciscodnacapphosting.Api()
    dnac_app.upload(tar=file, categories=categories)
    return


@cli.command("update")
@click.option("--id", required=True)
@click.option("--categories", required=True)
@click.pass_context
def update(ctx, id, categories):
    dnac_app = ciscodnacapphosting.Api()
    update = dnac_app.update(appId=id, categories=categories)
    return


@cli.command("delete")
@click.option("--id", required=True)
@click.pass_context
def delete(ctx, id):
    dnac_app = ciscodnacapphosting.Api()
    delete = dnac_app.delete(appId=id)
    return


@cli.command("docker")
@click.option("--download", required=False)
@click.option("--save/--no-save", default=False)
def docker(download, save):
    dnac_app = ciscodnacapphosting.Api()
    print(type(save))
    if download != None:
        print(download)
        if ":" in download:
            download = download.split(":")
            docker_download = dnac_app.docker.download(
                image=download[0], tag=download[1]
            )
        else:
            docker_download = dnac_app.docker.download(image=download, tag="latest")
        print(docker_download)
    if save is True:
        print("catch")
        save = dnac_app.docker.save(
            image=docker_download["image"], tag=docker_download["tag"]
        )
        print(save)
    return


if __name__ == "__main__":
    cli()